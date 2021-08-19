#找到图片中的人脸，并将其分别截取出来。
from PIL import Image
import face_recognition
import matplotlib.pyplot as plt
# Load the jpg file into a numpy array
image = face_recognition.load_image_file("/Users/xutao/Downloads/IMG_1574.JPG")

# Find all the faces in the image using the default HOG-based model.
# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# See also: find_faces_in_picture_cnn.py
face_locations = face_recognition.face_locations(image, model = 'cnn') #model为默空默认为hog，快但是不够准；cnn慢，但准确点。

print("{} face(s) is found in this photograph.".format(len(face_locations)))

for face_location in face_locations:
    print(face_location)
    # Print the location of each face in this image
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    face_image = image[top:bottom, left:right]
    # print(face_image.shape)
    pil_image = Image.fromarray(face_image)
    # pil_image.show()#MAC上出错
    plt.imshow(pil_image)
    plt.show()