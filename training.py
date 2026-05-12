import tensorflow as tf
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Data Augmentation for Training
train_gen = ImageDataGenerator(
    rescale=1./255, 
    rotation_range=20, 
    zoom_range=0.2, 
    horizontal_flip=True
)
val_gen = ImageDataGenerator(rescale=1./255)

# Load Datasets
train_data = train_gen.flow_from_directory("split_dataset/train", target_size=(150,150), batch_size=32, class_mode="categorical")
val_data = val_gen.flow_from_directory("split_dataset/val", target_size=(150,150), batch_size=32, class_mode="categorical")

# CNN Architecture
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(150,150,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5), 
    Dense(7, activation='softmax') 
])

# Compile & Train
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_data, validation_data=val_data, epochs=10)

# Save Model
os.makedirs("model", exist_ok=True)
model.save("model/garbage_model.keras")
print("Model saved successfully.")