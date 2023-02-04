
from keras.models import load_model
import numpy as np


def load_model(model_folder_path):
    model = load_model(model_folder_path + '/keras_model.h5')
    labels = open(model_folder_path + '/labels.txt', 'r').readlines()

    return model, labels


if __name__ == '__main__':
    model, labels = load_model('<model_folder_path>')
    probabilities = model.predict('<sample image path>')
    label = labels[np.argmax(probabilities)]
    most_possible_one_prob = max(probabilities[0])
    most_possible_one_prob = int(most_possible_one_prob * 100)
    most_possible_gesture = label.split()[-1]
    print(most_possible_gesture, most_possible_one_prob)
