#找到图片中的人脸，并将其在图片中圈起来。
import face_recognition
import matplotlib.pyplot as plt
import cv2
# Load the jpg file into a numpy array
# image = face_recognition.load_image_file("/Users/xutao/Documents/群众.jpg")
image=cv2.imread("/Users/xutao/Documents/群众.jpg")

face_locations = face_recognition.face_locations(image,  model = 'cnn')

print("{} face(s) is found in this photograph.".format(len(face_locations)))

for face_location in face_locations:
    print(face_location)
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 1) #绘制矩形框
cv2.imshow("output", image)
cv2.waitKey(0) #cv2中设置等待，否则图像无法加载。