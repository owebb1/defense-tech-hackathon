import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from joblib import dump

common_size = (64, 64)


folder_path = '/Users/owebb/defense-tech-hackathon/boat_wake_dataset'
data = []
labels = []

# Battleship
categories = ['carrier', 'patrol', 'submarine']
for category in categories:
    category_folder = os.path.join(folder_path, category)
    for image_filename in os.listdir(category_folder):
        image_path = os.path.join(category_folder, image_filename)
        image = Image.open(image_path)
        image = image.convert('L')
        image = image.resize(common_size)  # Resize the image
        image_array = np.array(image).flatten()
        data.append(image_array)
        labels.append(categories.index(category))

data = np.array(data)
labels = np.array(labels)

X_train, X_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, random_state=42)

# can swap out for any clustering model
clf = KNeighborsClassifier(n_neighbors=2)

clf.fit(X_train, y_train)

dump(clf, 'anomaly_detection_model.joblib')
