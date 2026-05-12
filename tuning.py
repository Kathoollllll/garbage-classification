import tensorflow as tf
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Tuning Hyperparameters
cfg = {"size": (150,150), "batch": 32, "epochs": 15, "drop": 0.3}

# Stronger Augmentation for Tuning
train_gen = ImageDataGenerator(rescale=1./255, rotation_range=30, zoom_range=0.3, horizontal_flip=True)
val_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory("split_dataset/train", target_size=cfg["size"], batch_size=cfg["batch"], class_mode='categorical')
val_data = val_gen.flow_from_directory("split_dataset/val", target_size=cfg["size"], batch_size=cfg["batch"], class_mode='categorical')

# CNN Architecture 
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(150,150,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(cfg["drop"]),
    Dense(7, activation='softmax')
])

# Compile & Train
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_data, validation_data=val_data, epochs=cfg["epochs"])

# Save Tuned Model
os.makedirs("model", exist_ok=True)
model.save("model/tuned_garbage_model.keras")
print("Tuned model saved!")