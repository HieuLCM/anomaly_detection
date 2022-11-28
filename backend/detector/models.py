from django.db import models
from django.conf import settings
from PIL import Image
import tensorflow as tf
import numpy as np
import cv2
import os
# Create your models here.

class Detector(models.Model):
    image = models.ImageField(upload_to='image')
    result = models.BooleanField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        
        img = Image.open(self.image)
        dimensions = (224, 224)
        resized_image = img.resize(dimensions).convert("RGB")
        ready_img = tf.keras.utils.img_to_array(resized_image)/255.
        file_model = os.path.join(settings.BASE_DIR, "ml_model/detector_model")
        model = tf.keras.models.load_model(file_model)
        reconstruction = model.predict(np.array([ready_img]))
        loss = tf.keras.losses.mae(reconstruction, np.array([ready_img]))
        threshold = np.load(os.path.join(settings.BASE_DIR, "ml_model/threshold.npy"))
        threshold_max = np.load(os.path.join(settings.BASE_DIR, "ml_model/threshold_max.npy"))
        print(np.mean(loss[0]))
        self.result = (threshold < np.mean(loss[0])) or (threshold_max < np.max(loss[0]))

        return super().save(*args, **kwargs)