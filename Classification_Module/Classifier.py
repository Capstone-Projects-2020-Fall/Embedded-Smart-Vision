import numpy as np
import pickle
import cv2 as cv
import os
import face_recognition


def initalize_embeddings():
    faces = dict()
    faces_directory = 'Classification_Module/Faces'
    for name in os.listdir(faces_directory):
        face_directory = os.path.join(faces_directory, name)

        if not os.path.isdir(face_directory):
            continue

        embeddings = list()

        for image_name in os.listdir(face_directory):
            path = os.path.join(face_directory, image_name)
            print("Loading " + path)
            image = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(image)
            if not len(encoding) > 0:
                print("Unable to find face")
                os.remove(path)
            else:
                print("Embedding created")
                embedding = encoding[0]
                embeddings.append(embedding)
            
        faces[name] = embeddings
    
    pickle.dump(faces, open("Classification_Module/Faces/embeddings", "wb"))


class Classifier:
    def __init__(self):
        if not os.path.isfile('Classification_Module/Faces/embeddings'):
            initalize_embeddings()
        self.faces = pickle.load(open('Classification_Module/Faces/embeddings', 'rb'))

    def __del__(self):
        pass

    def classify(self, frame, face_locations=None):
        tags = set()
        faces = face_recognition.face_encodings(frame, known_face_locations=face_locations, num_jitters=1, model="small")
        for face in faces:
            #print("Found a face!")
            for known_face in self.faces:
                results = face_recognition.compare_faces(self.faces[known_face], face)
                percent = results.count(True) / len(self.faces[known_face]) * 100
                if percent > 60:
                    tags.add(known_face)
        return tags

    def apply_tags(self, faces: list):
        tags = set()
        for face in faces:
            names = self.classify(face)
            for name in names:
                tags.add(name)
        if len(tags) == 0:
            tags.add('Unknown Person')
        return tags



if __name__ == '__main__':
    classifier = Classifier()
    test_image = face_recognition.load_image_file('Faces/Jimmy/Jimmy.jpg')
    test_tag = classifier.classify(test_image)
    print(test_tag)
