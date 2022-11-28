import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import layers, losses
from tensorflow.keras.models import Model
from PIL import Image
import os
import cv2

def load_dataset():
    data = []
    pills = os.listdir(os.getcwd() + "/pill/train/good/")
    # load the dataset
    for i in pills:
        imag = cv2.imread(os.getcwd() + "/pill/train/good/" + i)
        imag = cv2.cvtColor(imag, cv2.COLOR_BGR2RGB)
        img_from_array = Image.fromarray(imag, "RGB")
        resized_image = img_from_array.resize((224,224))
        data.append(np.array(resized_image))
    
    return np.array(data)

def prepare_dataset(data):
    # convert from integers to floats
    train_norm = data.astype('float32')
    
    # normalize to range 0-1
    train_norm = train_norm / 255.0

    # return normalized images
    return train_norm

train = load_dataset()

# prepare the dataset
train = prepare_dataset(train)
file_model = "./detector_model"
model = tf.keras.models.load_model(file_model)

reconstructions = model.predict(train)
train_loss = losses.mae(reconstructions, train)
mean_loss = np.array([np.mean(i) for i in train_loss])
max_loss = np.array([np.max(i) for i in train_loss])
threshold = np.mean(mean_loss) + np.std(mean_loss)
threshold_max = np.mean(max_loss) + np.std(max_loss)

print("Threshold : ", threshold)
print("Threshold Max : ", threshold_max)
np.save("threshold_max", np.array(threshold_max))