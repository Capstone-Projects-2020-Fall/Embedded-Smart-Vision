# import numpy as np
# import pickle
# import cv2 as cv
# import os
# import face_recognition
#
#
# class Classifier:
#     def __init__(self):
#         self.faces = dict()
#         face_directory = os.path.join('Classification_Module', 'Faces')
#         for image_name in os.listdir(face_directory):
#             path = os.path.join(face_directory, image_name)
#             image = face_recognition.load_image_file(path)
#             face = face_recognition.face_encodings(image)[0]
#             name = os.path.splitext(image_name)[0]
#             self.faces[name] = face
#
#     def __del__(self):
#         pass
#
#     def classify(self, frame, face_locations):
#         tags = set()
#         faces = face_recognition.face_encodings(frame, known_face_locations=face_locations, num_jitters=1, model="small")
#         for face in faces:
#             #print("Found a face!")
#             for known_face in self.faces:
#                 results = face_recognition.compare_faces([self.faces[known_face]], face)
#                 if results[0]:
#                     tags.add(known_face)
#         return tags
#
#     def apply_tags(self, faces: list):
#         tags = set()
#         for face in faces:
#             names = self.classify(face)
#             for name in names:
#                 tags.add(name)
#         if len(tags) == 0:
#             tags.add('Unknown Person')
#         return tags
#
#
# """
# if __name__ == '__main__':
#     classifier = Classifier()
#     test_image = face_recognition.load_image_file('test.jpg')
#     test_tag = classifier.classify(test_image)
#     print(test_tag)
# """