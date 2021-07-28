from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse

# Create your views here.
from django.urls import reverse
from threatify.models import *
from datetime import datetime,timedelta
import random as rd
import string
import imageio
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from twilio.rest import Client

account_sid = 'AC1e641a49104f38cad8e0ce8851f7dbf8' 
auth_token = '93b12157e0b858d7a6557230cb909875' 
client = Client(account_sid, auth_token) 

global feedGens
global model
global clipsCount
global compute
clipsCount = 0
feedGens = {}
model = vggCNNEncoder(num_classes=4)

model_dict = torch.load("./threatify/static/threatify/Weights/4-Way-Weighted-BestModel.pth")
model.load_state_dict(model_dict['Model'])
model.cuda()
model.eval()
compute = True


def Generator(Path, CameraID, Type, UserID):
    UserID = UserID
    UserDetails = User.objects.filter(UserID = UserID)[0]
    letters = string.ascii_lowercase
    tempCameraID = CameraID
    writeDirectory = "./threatify/static/threatify/storage/"
    tempPath = Path
    nFrame = 5
    sequence_length = 18
    while True:
        videoLength = -1
        framesProcessed = 0
        cam = cv2.VideoCapture(tempPath)
        if Type=="Recorded":
            #cam.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
            videoLength = cam.get(cv2.CAP_PROP_FRAME_COUNT)
            #cam.set(cv2.CAP_PROP_POS_AVI_RATIO,0)
            print("Starting Frame:",cam.get(cv2.CAP_PROP_FRAME_COUNT))
            print("Total Frames:",videoLength)
        # video = cv2.VideoWriter('./' + Path[:-3].split('/')[-1] + 'avi', cv2.VideoWriter_fourcc(*'DIVX'), 30,
        #                       (320, 240))
        ToTensor = torchvision.transforms.ToTensor()
        
        mask_length = 15
        remove_flag = False
        Frames = []
        totalFrames = []
        maxLengthTotal = nFrame * sequence_length
        font = cv2.FONT_HERSHEY_PLAIN
        crimeThreshold = 5
        crimeInstance = 0
        count = 0
        SIGMOID = nn.Sigmoid()
        video = None
        classes = {0: 'Fighting', 1: 'Gun Event', 2: 'Arson_Explosion', 3: 'Normal'}
        instanceCount = 0
        for data in ReadCamera(cam, nFrame):
            framesProcessed+=1
            idx, frame = data
            if idx == -1:
                if video is not None:
                    video.close()
                    video = None
                    if (tempCameraID!=-1):
                        FeedDetails = Feed.objects.filter(CameraID=tempCameraID)[0]
                        Object = ThreatLog(UserID=UserDetails, CameraID=FeedDetails,
                                            File=writePath, TimeStamp=datetime.now(), Category=Category,
                                            Type=Type)
                        Object.save()
                        message = client.messages.create(   
                                    messaging_service_sid='MG5c8a09954ec4b0a444a08b1f3fdd87f7',
                                    body="Threat Alert!\nThreat Type: "+str(Category.Threat)+"\nAssistance Needed ASAP.",      
                                    to=str(Category.ReportTo)
                                )
                        print("\n\n*************\n"+message.sid+"\n*************\n")
                    else:
                        Object = ThreatLog(UserID=UserDetails, File=writePath, TimeStamp=datetime.now(), Category=Category,
                                            Type=Type)
                        Object.save()
                    instanceCount+=1
                break
            elif idx % nFrame == 0:
                if count < mask_length:
                    count += 1
                Frames.append( frame)
                if framesProcessed>1:
                    x,y,d = frame.shape
                    mask = np.zeros((x, y))
                    Mask = np.zeros((x, y))
                    ReSize = torchvision.transforms.Resize((256, 256))
                    transformsInference = torchvision.transforms.Compose([
                        torchvision.transforms.Lambda(lambda crops: [Mask * crop for crop in crops]),
                        torchvision.transforms.Lambda(lambda crops: [PIL.Image.fromarray(crop, "RGB") for crop in crops]),
                        torchvision.transforms.Lambda(lambda crops: [ReSize(crop) for crop in crops]),
                        torchvision.transforms.Lambda(lambda crops: [ToTensor(crop) for crop in crops]),
                        torchvision.transforms.Lambda(lambda crops: torch.stack(crops)),
                        torchvision.transforms.Lambda(lambda crops: crops.unsqueeze(0)),
                    ])
                if len(Frames) > 1:
                    mask = masking(Frames[-1], Frames[-2], mask, remove_flag, mask_length, count)
                if len(Frames) == sequence_length:
                    remove_flag = True
                    Mask = np.zeros(Frames[0].shape, np.uint8)
                    Mask[mask > 0] = 1
                    if compute:
                        Images = transformsInference(Frames).cuda()
                        Output = model(Images)
                        T = SIGMOID(Output.to('cpu')).detach().numpy()
                        index = np.argmax(T[0])
                    #index = rd.randint(0, 3)
                    if index != 3 or crimeInstance > 0:
                        if crimeInstance == 0:
                            Category = Threat.objects.filter(ThreatID=index)[0]
                            fileName = ''.join(rd.choice(letters) for i in range(15))
                            writePath = writeDirectory + fileName + '.mp4'
                            # video = cv2.VideoWriter(writePath,
                            #                         cv2.VideoWriter_fourcc(*'DIVX'), 30, (320, 240))
                            video = imageio.get_writer(writePath, format='mp4', mode='I', fps=30)
                        if index != 3 and T[0][index] > 0.50:
                            crimeInstance = crimeThreshold

                        else:
                            index = 3
                            crimeInstance -= 1
                            if crimeInstance == 0:
                                video.close()
                                video = None
                                if (tempCameraID!=-1):
                                    FeedDetails = Feed.objects.filter(CameraID=tempCameraID)[0]
                                    Object = ThreatLog(UserID=UserDetails, CameraID=FeedDetails,
                                                        File=writePath, TimeStamp=datetime.now(), Category=Category,
                                                        Type=Type)
                                    Object.save()
                                    message = client.messages.create(   
                                                messaging_service_sid='MG5c8a09954ec4b0a444a08b1f3fdd87f7',
                                                body="Threat Alert!\nThreat Type: "+str(Category.Threat)+"\nAssistance Needed ASAP.",      
                                                to=str(Category.ReportTo)
                                            )
                                    print("\n\n*************\n"+str(Category.Threat)+"\n"+message.sid+"\n*************\n")
                                else:
                                    Object = ThreatLog(UserID=UserDetails, File=writePath, TimeStamp=datetime.now(), Category=Category,
                                                        Type=Type)
                                    Object.save()
                                
                                instanceCount+=1
            totalFrames.append(frame)
            if remove_flag:# and compute:
                if crimeInstance > 0:
                    if index != 3:
                        cv2.putText(totalFrames[0], classes[index], (5, 15), font, 1, (0, 0, 255), 1, cv2.LINE_4)
                        video.append_data(totalFrames[0])

                    else:
                        cv2.putText(totalFrames[0], classes[index], (5, 15), font, 1, (0, 255, 255), 1, cv2.LINE_4)
                        video.append_data(totalFrames[0])
                else:
                    cv2.putText(totalFrames[0], classes[index], (5, 15), font, 1, (255, 255, 255), 1, cv2.LINE_4)
                    # video.append_data(totalFrames[0])

            if idx % nFrame == 0 and len(Frames) == sequence_length:
                yield (totalFrames[0],int((framesProcessed/videoLength)*100),instanceCount)
                # if len(Frames) == sequence_length:
                del Frames[0]
            if len(totalFrames) == maxLengthTotal:
                del totalFrames[0]
        # video.release()
        print(Type)
        if Type=="Recorded":
            break
    yield (None,100,instanceCount)
    #raise StopIteration
            


feedsObjects = Feed.objects.all()

for feed in feedsObjects:
    feedGens[int(feed.CameraID)] = Generator(str(feed.Url), int(feed.CameraID),"Live",int(feed.UserID.UserID))

def checkSession(request):
    if request.session.has_key('UserID'):
        return True
    return False

def signin(request):
    if checkSession(request):
        return HttpResponseRedirect(reverse('camera'))
    else:
        context = {"Response": "", "Type": "text-danger"}
        if request.method == 'POST':
            form = request.POST
            Email = form.get('Email')
            Password = form.get('Password')
            Result = User.objects.filter(Email=Email, Password=Password)
            if Result:
                request.session['UserID'] = Result[0].UserID
                # return HttpResponse('<h1>Show Dashboard</h1>')
                return HttpResponseRedirect(reverse('camera'))
            else:
                context = {'Response': 'Invalid Email or Password...', "Type": "text-danger"}
        return render(request, 'threatify/SignIn.html', context)

def signup(request):
    # del request.session['UserID']
    if checkSession(request):
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        context = {"Response": "", "Type": "text-success"}
        if request.method == 'POST':
            form = request.POST
            Name = form.get('Name')
            Email = form.get('Email')
            Password = form.get('Password')
            Object = User(Name=Name, Email=Email, Password=Password)
            Object.save()
            context = {"Response": "Registration Successful. Go to Sign In Page...", "Type": "text-success"}
            return render(request, 'threatify/SignUp.html', context)
        return render(request, 'threatify/SignUp.html')

def inverse(request, inverseForm):
    if inverseForm == "signin":
        return HttpResponseRedirect(reverse('signup'))
    elif inverseForm == "signup":
        return HttpResponseRedirect(reverse('signin'))

def logout(request):
    if checkSession(request):
        del request.session['UserID']
    return HttpResponseRedirect(reverse('signin'))

def dashboard(request):
    if checkSession(request):
        return render(request, 'threatify/Dashboard.html')
    return HttpResponseRedirect(reverse('signin'))

def recorded(request):
    if checkSession(request):
        context = {}
        if request.method =="POST":
            files = request.FILES
            data = files['file'] # or self.files['image'] in your form
            path = default_storage.save('recorded/'+str(data), ContentFile(data.read()))
            print(path)
            context['upload'] = False
            context['fileName'] = str(path).split('/')[-1].split('.')[-2]
            print(context['fileName'])
            feedGens[context['fileName']] = Generator(str(path), int(-1),"Recorded",request.session['UserID'])
            return render(request, 'threatify/Recorded.html',context)
        else:
            context['upload'] = True
            return render(request, 'threatify/Recorded.html',context)
    return HttpResponseRedirect(reverse('signin'))

def processRecorded(request, fileName):
    max = datetime.now() + timedelta(seconds = 2)
    threatCount = 0
    while(datetime.now()<max):
        #try:
        _ , percentage, threatCount = next(feedGens[fileName])
        data = json.dumps({'percentage': percentage,'threatCount':threatCount})
        if percentage==100:
            break
        #except StopIteration:
            #print("EXCEPTION CATCHED")
           # data = json.dumps({'percentage': 100,'threatCount': threatCount})
            #break
    print(data)
    return HttpResponse(data)

def camera(request):
    if checkSession(request):
        UserID = request.session['UserID']
        feedObjects = Feed.objects.filter(UserID=UserID)
        feedsUrl = []
        feedsId = []
        feedsUserName = []
        feedsPassword = []
        feedsLocation = []
        types = []
        for feed in feedObjects:
            feedsUrl.append(feed.Url)
            feedsId.append(feed.CameraID)
            feedsUserName.append(feed.Username)
            feedsPassword.append(feed.Password)
            feedsLocation.append(feed.CameraLocation)
            if 'youtube' in feed.Url:
                types.append('Youtube')
            elif 'http' in feed.Url:
                types.append('IP-Camera')
            else:
                types.append('CCTV')
        context = {
            "Feeds": zip(feedsId, feedsLocation, feedsUrl, types),
            "Updates": zip(feedsId, feedsLocation, feedsUrl, feedsUserName, feedsPassword),
            "None": feedsId,
        }
        return render(request, 'threatify/Camera.html', context)
    return HttpResponseRedirect(reverse('signin'))


def cameraModify(request, function):
    if checkSession(request):
        if request.method == 'POST':
            UserID = User.objects.get(UserID=request.session["UserID"])
            if function == "add":
                form = request.POST
                Location = form.get("Location")
                URL = form.get("URL")
                UserName = form.get("UserName")
                Password = form.get("Password")
                Object = Feed(UserID=UserID, CameraLocation=Location, Url=URL, Username=UserName, Password=Password)
                Object.save()
                feedGens[Object.CameraID] = Generator(URL, Object.CameraID,"Live",UserID.UserID)

            elif function == "update":
                form = request.POST
                CameraID = form.get("feedsDropDown")
                Location = form.get("Location")
                URL = form.get("URL")
                UserName = form.get("UserName")
                Password = form.get("Password")
                Feed.objects.filter(CameraID=CameraID).update(CameraLocation=Location, Url=URL, Username=UserName,
                                                              Password=Password)
            elif function == "delete":
                form = request.POST
                CameraID = form.get("feedsDropDown2")
                Feed.objects.filter(CameraID=CameraID).delete()
                del feedGens[int(CameraID)]
            return HttpResponseRedirect(reverse('camera'))
        else:
            return HttpResponseRedirect(reverse('camera'))
    return HttpResponseRedirect(reverse('signin'))


def threatLog(request):
    if checkSession(request):
        if request.method == "GET":
            UserID = request.session['UserID']
            threatLogObjects = ThreatLog.objects.filter(UserID=UserID)

            threatIDs = []
            cameraIDs = []
            filePaths = []
            timeStamps = []
            categories = []
            durations = []
            confidences = []

            for threat in threatLogObjects:
                threatIDs.append(threat.ThreatID)
                cameraIDs.append(threat.CameraID)
                filePaths.append('/'.join(threat.File.split('/')[3:]))
                timeStamps.append(threat.TimeStamp)
                categories.append(str(threat.Category))
                durations.append(threat.Duration)
                confidences.append(threat.Confidence)
            context = {
                "threatLogs": zip(threatIDs, cameraIDs, filePaths, timeStamps, categories, durations, confidences)
            }
        elif request.method == "POST":
            UserID = request.session['UserID']
            form = request.POST
            threatLogObjects = ThreatLog.objects.filter(UserID=UserID)
            for threatLogObject in threatLogObjects:
                if form.get(str(threatLogObject.ThreatID)) == "on":
                    ThreatLog.objects.filter(ThreatID=threatLogObject.ThreatID).delete()
            threatLogObjects = ThreatLog.objects.filter(UserID=UserID)
            threatIDs = []
            cameraIDs = []
            filePaths = []
            timeStamps = []
            categories = []
            durations = []
            confidences = []
            for threat in threatLogObjects:
                threatIDs.append(threat.ThreatID)
                cameraIDs.append(threat.CameraID)
                filePaths.append('/'.join(threat.File.split('/')))
                timeStamps.append(threat.TimeStamp)
                categories.append(str(threat.Category))
                durations.append(threat.Duration)
                confidences.append(threat.Confidence)
            context = {
                "threatLogs": zip(threatIDs, cameraIDs, filePaths, timeStamps, categories, durations,
                                  confidences)
            }
        return render(request, 'threatify/ThreatLog.html', context)
    return HttpResponseRedirect(reverse('signin'))


def settings(request):
    return HttpResponse('<h1>Show settings</h1>')


def findThreat(request, feedID):
    try:
        Frame,_,_ = next(feedGens[feedID])
    except StopIteration:
        print("Stop Iteration Caught for feed:",feedID)
    Frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
    pil_image = to_image(Frame)
    image_uri = to_data_uri(pil_image)
    data = json.dumps({'frame': image_uri})
    return HttpResponse(data)
