import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Load trained model
model = tf.keras.models.load_model('model/garbage_model.keras')

# Preprocess Image
img_path = 'split_dataset/test/Clothes/clothes2.jpg' 
img = image.load_img(img_path, target_size=(150, 150))
img_array = image.img_to_array(img) / 255
img_array = np.expand_dims(img_array, axis=0) 

# Predict
preds = model.predict(img_array)
labels = ['battery', 'cardboard', 'clothes', 'glass', 'metal', 'paper', 'plastic'] 

# Result
print(f"Predicted: {labels[np.argmax(preds)]}")
print(f"Accuracy: {np.max(preds)*100:.2f}%")