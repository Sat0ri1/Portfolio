""" Distinguishing Theraphosidae species with CNN, Paweł Grygielski """

# Importing libs
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define data generators for training and validation
train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

# Paths to datasets
train_path = ''
test_path = ''

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
"""Convolutional Layer (Conv2D):
Filters (32, 64, 128, etc.): The number of filters determines the depth of the output volume.
Kernel Size ((3, 3), (5, 5), etc.): The size of the convolutional filters, influencing the size of the learned features.
Activation ('relu', 'sigmoid', etc.): The activation function applied element-wise to the output.

More Filters (64, 128, etc.): Increasing the number of filters allows the model to learn more complex features. 
However, it also increases the computational cost.
Fewer Filters (16, etc.): Reducing the number of filters may lead to the model learning simpler features, 
potentially underfitting the data.

Larger Kernel ((5, 5), (7, 7), etc.): Larger kernels capture more spatial context 
but may increase the number of parameters and computational load.
Smaller Kernel ((3, 3), (2, 2), etc.): Smaller kernels focus on local features, reduce parameters, 
and can be computationally more efficient.

^^^Purpose: Extract features from input images using convolutional filters^^^

ReLU ('relu'): Commonly used for its simplicity and effectiveness in promoting non-linearity.
Sigmoid ('sigmoid'): Suitable for binary classification tasks, but may suffer from vanishing gradient problems in deep networks.
Tanh ('tanh'): Similar to sigmoid but with a higher output range, potentially mitigating vanishing gradient issues.

Larger Pool Size ((3, 3), (4, 4), etc.): Increases downsampling, reducing spatial dimensions but potentially discarding fine details.
Smaller Pool Size ((2, 2), (1, 1), etc.): Less downsampling, retains more spatial information, but may increase computational load.
^^^Purpose: Downsample the spatial dimensions, reducing computation and controlling overfitting.^^^"""
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Flatten layer
model.add(layers.Flatten())
"""^^^Purpose: Flatten the output from the convolutional layers into a 1D vector for input to the dense layers.^^^ """
# Dense layers

"""More Units (256, 512, etc.): Increases the capacity of the model to learn complex representations.
Fewer Units (64, 128, etc.): Reduces model capacity, potentially underfitting complex patterns.
^^^Purpose: Fully connected layer for high-level reasoning.^^^"""

model.add(layers.Dense(128, activation='relu'))

num_classes = 300 # Adjust num_classes based on the number of tarantula species
model.add(layers.Dense(num_classes, activation='softmax'))  

# Something to add if needed: 
"""DROPOUT RATE: Higher Dropout Rate (0.5, 0.6, etc.): Increases regularization, preventing overfitting but may slow down convergence.
Lower Dropout Rate (0.2, 0.3, etc.): Less regularization, faster convergence, but may be prone to overfitting.
^^^Purpose: Regularization technique to prevent overfitting by randomly setting a fraction of input units to zero during training.^^^"""
            # model.add(layers.Dropout(0.5)) BETWEEN THE DENSE LAYERS

"""BATCH NORMALIZATION: Included (layers.BatchNormalization()): Can stabilize and accelerate training by normalizing input distributions.
Not Included: May require more careful weight initialization and learning rate tuning.
^^^Purpose: Normalize the activations of the previous layer to improve training stability and speed up convergence.^^^"""
            # model.add(layers.BatchNormalization())
# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
#TRAINING
epochs = 10  # Number of iterations
model.fit(train_generator, epochs=epochs, validation_data=test_generator)

#EVALUATING
test_loss, test_acc = model.evaluate(test_generator)
print(f'Test accuracy: {test_acc}')

#PREDICTING
predictions = model.predict(test_generator)

#SAVING MODEL
#model.save('model.h5')