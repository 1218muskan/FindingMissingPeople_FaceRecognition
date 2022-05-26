import cv2
import face_recognition
import json
import os

# opening config.json file in reading mode
with open('config.json', 'r') as c:
    params = json.load(c)["params"]


# fn to detect the number of faces in the image
def detectFace(imgLoc):

    image = face_recognition.load_image_file(imgLoc)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    faceLoc = face_recognition.face_locations(image)
    # returns a list of tuple of face location for all the faces in image

    return len(faceLoc)




# this function called in match_faces function
def getFaceEncodings(images):
    encodingList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodingList.append(encode)

    return encodingList



def match_faces(suspect_img_loc, missing_img_name):

    # importing images
    suspect_img = face_recognition.load_image_file( params['suspect_images'] + suspect_img_loc )
    suspect_img = cv2.cvtColor(suspect_img, cv2.COLOR_BGR2RGB)

    # getting encoding of suspect image
    suspect_encoding = face_recognition.face_encodings(suspect_img)

    # loading missing people images
    dbImages = []
    missingPeopleNames = []

    for mNames in missing_img_name:
        currImg = cv2.imread( params['missing_images'] + mNames )
        dbImages.append(currImg)
        missingPeopleNames.append(mNames)
        # missingPeopleNames.append(os.path.splitext(mNames)[0])


    missingEncodings = getFaceEncodings(dbImages)

    index = 0
    for en in missingEncodings:
        for sEN in suspect_encoding:

            result = face_recognition.compare_faces([en], sEN)
            if result[0]:
                return missingPeopleNames[index]

        index += 1

    return False



# missingEncodings - list of encodings of all missing person
# en - encoding of 1 missing person from database

# suspect_encoding: encoding list we got from suspect image ( its length equal to no. of faces in that image )
# sEN: encoding of single face





