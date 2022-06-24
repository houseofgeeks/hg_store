from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from pathlib import Path


class Nsfw:
	def __init__(self):
		self.model = tf.keras.models.load_model("./nsfw/NSFW_Abhinav_Final.h5", custom_objects=None, compile=True, options=None)
	def predict(self,image):
		predictions = self.model.predict(image)
		return np.round(predictions)
