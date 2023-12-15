"""USING THE TRAINED MODEL"""

#Loading necessary packages
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

loaded_model = load_model('model.h5')

# Path to the new image
new_image_path = ''

# Loading and preprocessing the image
img = image.load_img(new_image_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.  # Rescale to match the training data normalization

# Now 'img_array' is a preprocessed image we can pass to model to recognize the species
predictions = loaded_model.predict(img_array)

# Print prediction
print(predictions)