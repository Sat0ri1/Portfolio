""" Distinguishing Theraphosidae species with CNN, Paweł Grygielski """

# Importing libs
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical

# Define data generators for training and validation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2, 
    brightness_range=[0.8, 1.2]  
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Paths to datasets
train_path = 'C:/Users/pgryg/Desktop/CNN_project/Species'
test_path = 'C:/Users/pgryg/Desktop/CNN_project/test'

# Create generators for training and validation
train_generator = train_datagen.flow_from_directory(train_path,
                                                    target_size=(224, 224),  # Adjust based on your image size
                                                    batch_size=32,
                                                    class_mode='categorical')

test_generator = test_datagen.flow_from_directory(test_path,
                                                  target_size=(224, 224),
                                                  batch_size=32,
                                                  class_mode='categorical')

model = models.Sequential()

# Convolutional layers

model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Flatten layer
model.add(layers.Flatten())

# Dense layers
model.add(layers.Dense(256, activation='relu'))

num_classes = 2 # Number of species
model.add(layers.Dense(num_classes, activation='softmax'))  

# Something to add if needed: 
    # model.add(layers.Dropout(0.5)) BETWEEN THE DENSE LAYERS
    # model.add(layers.BatchNormalization())

# One-hot encode
y_train_encoded = to_categorical(train_generator.classes, num_classes)
y_test_encoded = to_categorical(test_generator.classes, num_classes)

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
#TRAINING
epochs = 20  # Number of iterations
model.fit(train_generator, epochs=epochs, validation_data=test_generator)

#EVALUATING
test_loss, test_acc = model.evaluate(test_generator)
print(f'Test accuracy: {test_acc}')

#PREDICTING
predictions = model.predict(test_generator)

#SAVING
model.save('model.h5')
#Flouders <3
