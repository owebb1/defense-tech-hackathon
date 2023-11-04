import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
import os


folder_path = 'path/to/your/images/folder'

dataset = []


def rgb_to_grayscale(rgb_array):
    if rgb_array.ndim == 3 and rgb_array.shape[2] == 3:
        grayscale_array = np.dot(rgb_array[..., :3], [0.2989, 0.5870, 0.1140])
        return grayscale_array
    else:
        raise ValueError(
            "Input array must be an RGB image with three channels")


for image_filename in os.listdir(folder_path):
    image_path = os.path.join(folder_path, image_filename)
    if image_path.lower().endswith('.png', '.jpg', '.jpeg'):
        img = Image.open(image_path)
        rgb_img = img.convert('RGB')
        rgb_array = np.array(rgb_img)
        grayscale_array = rgb_to_grayscale(rgb_array).flatten()
        dataset.append(grayscale_array)

        label_arr = [image_filename]

dataset_array = np.array(dataset)
labels = np.array(label_arr)


# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    dataset_array, labels, test_size=0.2, random_state=42)
