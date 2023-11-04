import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump


folder_path = '/Users/owebb/defense-tech-hackathon/boat_wake_dataset'
data = []
labels = []


categories = ['carrier', 'cruiser', 'destroyer', 'battleship']
for category in categories:
    category_folder = os.path.join(folder_path, category)
    for image_filename in os.listdir(category_folder):
        image_path = os.path.join(category_folder, image_filename)
        image = Image.open(image_path)
        image = image.convert('L')
        image_array = np.array(image)
        data.append(image_array)
        labels.append(categories.index(category))

data = np.array(data)
labels = np.array(labels)

X_train, X_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.5, random_state=42)

clf = RandomForestClassifier()

clf.fit(X_train, y_train)


dump(clf, 'anomaly_detection_model.joblib')
