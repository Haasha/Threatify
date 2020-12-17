# Threatify

  ## Introduction
  Threatify aims to provide a new mode of surveillance. It aims to shift from manual surveillance to Deep Learning based surveillance where deep learning based models are responsible for identifying and classifying threat from a CCTV feed.

  ## Dataset
  The dataset that we are using is **[UCF-Crime Dataset](https://www.crcv.ucf.edu/projects/real-world/)**. This is a video dataset containing CCTV videos. It has a total of 14 classes i.e. Abuse, Arrest, Arson, Assault, Burglary, etc. including Normal Event too. The classes that we are focusing on are:
  1. Fighting
  2. Gun-Event
  3. Arson & Explosion
  4. Normal Event

  ### Fighting
  ![Gif of Fighting](/attachments/fighting.gif)

  ### Gun-Event
  ![Gif of Gun-Event](/attachments/shooting.gif)

  ### Arson & Explosion
  ![Gif of Arson & Explosion](/attachments/arson.gif)

  ### Normal Event
  ![Gif of Normal Event](/attachments/normal.gif)

### Model Architecture
  The model that we are using is basically composed of two chunks. Vgg16 which acts as Feature Extraction and then we have our Classifying block which identifies which type of video it was. 
  ![Gif of Normal Event](/attachments/Architecture.png)
  
### Video Segmentation
  We are using openCV for video segmentation. The approach we follow is to identify the motion from the video. We do this by taking absolute difference in series of frames and combining those results to get a well segmented portion. This approach is very fast. We were able to process 400+ Frames through this video segmentation technique in one Second.
  ![Video Segmentation](/attachments/Segmentation.jpg)
  

### Approach
  The video is fetched firstly. Once we have that, we send it through our video segmenting which eliminates non moving part. Then it is sent to pretrained vgg16 pytorch model for feature extraction. Those extracted features are sent to our classifying block which consists of Fully Connected Layers and LSTM block. LSTM identifies the relation between series of frames and FC layers help in classifying it.
  
