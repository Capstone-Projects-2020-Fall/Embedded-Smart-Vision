import tensorflow as tf
import numpy as np
import sklearn
import pickle
from keras_facenet import FaceNet
import cv2 as cv



class Classifier:
    def __init__(self):
        self.embedding_model = FaceNet()
        self.classifier_model = pickle.load(open('Classification_Module/face_classifier', 'rb'))

    def __del__(self):
        pass

    def classify(self, embedding):
        embedding = embedding.reshape(1, -1)
        classification = self.classifier_model.predict(embedding)
        proba = self.classifier_model.predict_proba(embedding)
        prob = proba[0, classification[0]] * 100

        return classification, prob

    def apply_tags(self, faces: list):
        tags = set()
        faces = np.asarray(faces)
        print('Attempting to grab embeddings')
        embeddings = self.embedding_model.embeddings(faces)
        print('Attempting to classify embeddings')
        for embedding in embeddings:
            tag, prob = self.classify(embedding)
            if prob < 60.000:
                tags.add('Unknown')
            else:
                if tag == 0:
                    tags.add('Amanda')
                elif tag == 1:
                    tags.add('Jimmy')
        return tags
