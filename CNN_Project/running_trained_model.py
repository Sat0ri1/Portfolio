"""USING THE TRAINED MODEL"""

# Loading necessary packages
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

loaded_model = load_model('model.h5')

# Path to the new image
new_image_path = input("Podaj sciezke do zdjecia: ")
#C:/Users/pgryg/Desktop/

# Loading and preprocessing the image
img = image.load_img(new_image_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.  # Rescale to match the training data

# Now 'img_array' is a preprocessed image we can pass to model to recognize the species
predictions = loaded_model.predict(img_array)

# Class labels - Species names
class_labels = ["Chilobrachys natanicharum", "Poecilotheria metallica"]

# Get the index of the class with the highest probability
predicted_class_index = np.argmax(predictions)

# Get the corresponding class label
predicted_class_label = class_labels[predicted_class_index]

# Print the prediction
print(f"The predicted class is: {predicted_class_label}")

# Print prediction
print(predictions)
