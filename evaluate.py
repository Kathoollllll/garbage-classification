import tensorflow as tf
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

# Load the model you want to evaluate
model = tf.keras.models.load_model("model/garbage_model.keras")
gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

# Tuning
# val_data = gen.flow_from_directory("split_dataset/val", target_size=(128,128), batch_size=32, class_mode="categorical", shuffle=False)
# val_loss, val_acc = model.evaluate(val_data)
# print(f"Validation Accuracy: {val_acc*100:.2f}%")

# Final Test Evaluation
test_data = gen.flow_from_directory("split_dataset/test", target_size=(150,150), batch_size=32, class_mode="categorical", shuffle=False)

loss, acc = model.evaluate(test_data)
print(f"\nFinal Test Accuracy: {acc*100:.2f}%")

# Detailed Predictions
preds = model.predict(test_data)
y_pred = np.argmax(preds, axis=1)
labels = list(test_data.class_indices.keys())

print("\nConfusion Matrix:\n", confusion_matrix(test_data.classes, y_pred))
print("\nClassification Report:\n", classification_report(test_data.classes, y_pred, target_names=labels))