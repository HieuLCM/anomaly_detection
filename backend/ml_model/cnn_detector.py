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

# Define a convilutional autoencoder
class Detector(Model):
  def __init__(self):
    super(Detector, self).__init__()
    self.encoder = tf.keras.Sequential([
      layers.Input(shape=(224, 224, 3)),
      layers.Conv2D(64, (3,3),padding="same", activation="relu"),
      # layers.MaxPool2D(pool_size=(2,2)),
      layers.Conv2D(128, (3,3),padding="same", activation="relu"),
      layers.MaxPool2D(pool_size=(2,2)),
      layers.Conv2D(256, (3,3),padding="same", activation="relu"),
      layers.MaxPool2D(pool_size=(2,2)),
    ])

    self.decoder = tf.keras.Sequential([
      layers.Conv2DTranspose(256, (3,3), strides=2, activation='relu', padding='same'),
      layers.Conv2DTranspose(128, (3,3), strides=2, activation='relu', padding='same'),
      layers.Conv2DTranspose(64, (3,3), activation='relu', padding='same'),
      layers.Conv2DTranspose(3, (3,3), activation='sigmoid', padding='same'),
    ])

  def call(self, x):
    encoded = self.encoder(x)
    decoded = self.decoder(encoded)
    return decoded

# train, evaluate and save the model
def train_and_save_model(train):
    # define the model
    model = Detector()
    model.compile(optimizer='adam', loss=losses.MeanSquaredError())
    # train the model
    history = model.fit(
      train,
      train,
      epochs=100, 
      batch_size=8, 
      validation_split=0.2,
      shuffle=True,
    )
    
    # evaluate the model on test data
    print(history)

    reconstructions = model.predict(train)
    train_loss = losses.mae(reconstructions, train)
    mean_loss = np.array([np.mean(i) for i in train_loss])
    max_loss = np.array([np.max(i) for i in train_loss])
    threshold = np.mean(mean_loss) + np.std(mean_loss)
    threshold_max = np.mean(max_loss) + np.std(max_loss)
    print("Threshold : ", threshold)
    np.save("threshold", np.array(threshold))
    print("Threshold Max : ", threshold_max)
    np.save("threshold_max", np.array(threshold_max))
    # save the model
    model.save('detector_model', save_format="tf")
    print('Saved model to disk')

# run the test harness for evaluating the model
def run_test_harness():
    # load the dataset
    train = load_dataset()
    
    # prepare the dataset
    train = prepare_dataset(train)
    
    # train, evaluate and save the model
    train_and_save_model(train)


# entry point, run the test harness
run_test_harness()