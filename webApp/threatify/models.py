from django.db import models
from timezone_field import TimeZoneField
from django_countries.fields import CountryField
from django.core import validators
import torch
import torchvision
import torch.nn as nn
import cv2
import numpy as np
from PIL import Image
import io
from io import BytesIO
import base64
import numpy as np
import PIL
import json

Types = (('1', 'Live'), ('2', 'Recorded'))


# Create your models here.
class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=254)
    Password = models.CharField(max_length=100)
    Phone = models.CharField(max_length=20, blank=True)
    SSN = models.CharField(max_length=50, blank=True)
    AddressLine1 = models.CharField(max_length=50, blank=True)
    AddressLine2 = models.CharField(max_length=50, blank=True)
    City = models.CharField(max_length=50, blank=True)
    Country = CountryField(blank_label='(select country)', blank=True)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0.0)
    Latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0.0)
    TimeZone = TimeZoneField(choices_display='WITH_GMT_OFFSET', blank=True)
    MotionDetection = models.BooleanField(default=False)
    MotionAlert = models.BooleanField(default=False)
    MotionSensitivity = models.IntegerField(
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)], default=0)

    CrimeDetection = models.BooleanField(default=False)
    CrimeAlert = models.BooleanField(default=False)
    CrimeSensitivity = models.IntegerField(
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)], default=0)

    def __str__(self):
        return str(self.UserID) + '_' + self.Name


class Feed(models.Model):
    CameraID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    CameraLocation = models.CharField(max_length=50)
    Url = models.URLField(validators=[validators.URLValidator])
    Username = models.CharField(max_length=100, blank=True)
    Password = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.UserID) + '_' + str(self.CameraID)


class Threat(models.Model):
    ThreatID = models.IntegerField(primary_key=True)
    Threat = models.CharField(max_length=100)
    ReportTo = models.CharField(max_length=100)

    def __str__(self):
        return str(self.Threat)


class ThreatLog(models.Model):
    ThreatID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    CameraID = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True)
    File = models.CharField(max_length=300)
    TimeStamp = models.DateTimeField()
    Category = models.ForeignKey(Threat, on_delete=models.CASCADE)
    Duration = models.DurationField(blank=True, null=True)

    Confidence = models.FloatField(blank=True, null=True)
    Type = models.CharField(max_length=8, choices=Types, default=Types[0])

    def __str__(self):
        return str(self.UserID) + '_' + str(self.ThreatID)


class vggCNNEncoder(nn.Module):
    def __init__(self, fc_hidden1=512, fc_hidden2=512, drop_p=0.3, CNN_embed_dim=300, h_RNN_layers=3, h_RNN=256,
                 h_FC_dim=128, num_classes=3):
        """Load the pretrained ResNet-152 and replace top fc layer."""
        super(vggCNNEncoder, self).__init__()

        self.fc_hidden1, self.fc_hidden2 = fc_hidden1, fc_hidden2
        self.drop_p = drop_p
        self.RNN_input_size = CNN_embed_dim
        self.h_RNN_layers = h_RNN_layers  # RNN hidden layers
        self.h_RNN = h_RNN  # RNN hidden nodes
        self.h_FC_dim = h_FC_dim
        self.drop_p = drop_p
        self.num_classes = num_classes
        # loading vgg16 model
        vgg16 = torchvision.models.vgg16(pretrained=False)
        # delete the last fc layer.
        modules = list(vgg16.children())[:-1]
        self.vgg16 = nn.Sequential(*modules)
        # defining layers for decoder
        self.fc1 = nn.Linear(vgg16.classifier[0].in_features, fc_hidden1)
        self.bn1 = nn.BatchNorm1d(fc_hidden1, momentum=0.01)
        self.fc2 = nn.Linear(fc_hidden1, fc_hidden2)
        self.bn2 = nn.BatchNorm1d(fc_hidden2, momentum=0.01)
        self.fc3 = nn.Linear(fc_hidden2, CNN_embed_dim)
        # LSTM layer for sequential understanding
        self.LSTM = nn.LSTM(
            input_size=self.RNN_input_size,
            hidden_size=self.h_RNN,
            num_layers=h_RNN_layers,
            batch_first=True)
        # input & output will has batch size as 1s dimension. e.g. (batch, time_step, input_size))
        # layers for classification
        self.fc4 = nn.Linear(self.h_RNN, self.h_FC_dim)
        self.fc5 = nn.Linear(self.h_FC_dim, self.num_classes)

    def forward(self, x_3d):
        cnn_embed_seq = []
        for t in range(x_3d.size(1)):
            with torch.no_grad():
                x = self.vgg16(x_3d[:, t, :, :, :])  # ResNet
                x = x.view(x.size(0), -1)  # flatten output of conv

            # FC layers
            x = self.bn1(self.fc1(x))
            x = nn.functional.relu(x)
            x = nn.functional.dropout(x, p=self.drop_p, training=self.training)
            x = self.bn2(self.fc2(x))
            x = nn.functional.relu(x)
            x = nn.functional.dropout(x, p=self.drop_p, training=self.training)
            x = self.fc3(x)

            cnn_embed_seq.append(x)
        cnn_embed_seq = torch.stack(cnn_embed_seq, dim=0).transpose_(0, 1)

        self.LSTM.flatten_parameters()
        RNN_out, (h_n, h_c) = self.LSTM(cnn_embed_seq, None)
        x = self.fc4(RNN_out[:, -1, :])  # choose RNN_out at the last time step
        x = nn.functional.relu(x)
        x = nn.functional.dropout(x, p=self.drop_p, training=self.training)
        x = self.fc5(x)
        return x


def ReadCamera(camera, nFrame):
    count = 0
    while True:
        (grabbed, frame) = camera.read()

        if grabbed:
            count += 1
            yield (count, frame)
            if count % nFrame == 0:
                count = 0
        else:
            print("FRAME NOT FOUND")
            yield (-1, frame)


def masking(new_frame, prev_frame, mask, remove_flag, mask_length, count):
    zero_frame = len(new_frame[new_frame == 0])
    dimension = new_frame.shape[0] * new_frame.shape[1] * new_frame.shape[2]
    new_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
    new_gray = cv2.GaussianBlur(new_gray, (3, 3), 0)
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (3, 3), 0)
    deltaframe = cv2.absdiff(new_gray, prev_gray)
    if count < mask_length:
        i = count
    else:
        i = mask_length
    if remove_flag == 1:
        mask[mask > 0] -= 1
    threshold = cv2.threshold(deltaframe, 15, i, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, 20)
    if zero_frame < dimension:
        mask = np.maximum(mask, threshold)
    return mask


def to_data_uri(pil_img):
    data = BytesIO()
    pil_img.save(data, "PNG")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,' + data64.decode('utf-8')


def to_image(numpy_img):
    img = Image.fromarray(numpy_img, 'RGB')
    return img
