import cv2
import time
import os
import redis
import json

configFileLocation = os.getenv('alarm_config_location') 
if not configFileLocation :
    configFileLocation = '../appsettings.json'
    
configFile = open(configFileLocation)
config = json.load(configFile)
img_folder = config['Camera']['ImageFolder']
r = redis.Redis(host=config['Redis']['ip'], port=config['Redis']['port'], db=0, password=config['Redis']['password'])
r_pubsub = r.pubsub()

# Initializing the HOG person 
# detector 
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def imageCallback(self):
    global hog
    imgToProcessFileName = str(self['data'],'utf-8')
    imgToProcess = img_folder + imgToProcessFileName
    print('processing: ' + imgToProcess)
    image = cv2.imread(imgToProcess)
        # Detecting all the regions 
        # in the Image that has a 
        # pedestrians inside it 
    (regions, weights) = hog.detectMultiScale(image,
                                        winStride=(4, 4),
                                        padding=(10, 10),
                                        scale=1.2)

    # Drawing the regions in the 
    # Image 
    for (x, y, w, h) in regions:
        cv2.rectangle(image, (x, y),
                    (x + w, y + h),
                    (0, 0, 255), 0)
        
        # Showing the output Image
    if len(regions) > 0:
        new_img_name = imgToProcessFileName.replace('.jpg','_MATCHED.jpg')
        cv2.imwrite(img_folder + new_img_name ,image)
        print ('People detected '+new_img_name)
        r.publish('PERSON_DETECTED',new_img_name)
            
r_pubsub.subscribe(**{'IMAGE_CAPTURED':imageCallback})
r_pubsub.run_in_thread(sleep_time=0.001)

while True:
    time.sleep(1)