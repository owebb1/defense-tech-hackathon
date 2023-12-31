from joblib import load
from flask import Flask, render_template, jsonify
import numpy as np
import sqlite3
import cv2
import tensorflow as tf
# from object_detection.utils import config_util
import numpy as np
import matplotlib.pyplot as plt
# Now, on your device, you would load the model
model = load('anomaly_detection_model.joblib')
ships = ['carrier', 'cruiser', 'submarine', 'battleship']

app = Flask(__name__)


# can use your own pretrained model here for CV portion, but this will give accurate results on ships for now
# model_name = 'ssd_mobilenet_v2_coco_2018_03_29'  # Example model
# pipeline_config = model_name + '/pipeline.config'
# model_dir = model_name + '/checkpoint'

# # configs = config_util.get_configs_from_pipeline_file(pipeline_config)
# model_config = configs['model']
# detection_model = tf.saved_model.load(model_dir)

# SQLite DB Creation
conn = sqlite3.connect('ships_data.db')
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE IF NOT EXISTS ship_detections
             (timestamp DATETIME, ship_type TEXT, confidence REAL, image_path TEXT)''')


def retrieve_data_from_accelerometer():
    # Generate the sample accelerometer data
    # Sample rate and time vector
    fs = 1000  # Sample rate in Hz
    t = np.arange(0, 40, 1/fs)  # Time vector for 10 seconds

    # Sine wave parameters
    A1, A2, A3, A4 = 0.5, 0.5, 0.5, 1  # Amplitudes
    f1, f2, f3, f4 = 1, 1, 1, 1  # Frequencies in Hz
    p1, p2, p3, p4 = -0.226*np.pi, np.pi, np.pi * \
        0.226, np.pi  # Phase shifts in radians

    # Generate the sine waves
    wave1_accel1 = A1 * np.sin(2 * np.pi * f1 * t + p1)
    # wave1_accel2 = A2 * np.sin(2 * np.pi * f2 * t + p2)
    # wave1_accel3 = A3 * np.sin(2 * np.pi * f3 * t + p3)
    # wave1_accel4 = wave1_accel2

    f1, f2, f3, f4 = 0.5, 0.5, 0.5, 0.5  # Frequencies in Hz
    p1, p2, p3, p4 = np.pi, -0.226*np.pi, np.pi, np.pi * \
        0.226  # Phase shifts in radians

    A = 1      # Amplitude
    alpha = 0.1  # Decay factor
    f = 0.5     # Frequency (Hz)
    lambda_ = 2  # Wavelength (m)
    c = lambda_ * f  # Wave speed = wavelength * frequency
    x0 = 0      # Initial position (m)
    phi = -2 * np.pi * x0 / lambda_
    # wave_full1 = A1 * np.sin(2 * np.pi * f1 * t + p1)
    # wave_full2 = A2 * np.sin(2 * np.pi * f2 * t + p2)
    # wave_full4 = A4 * np.sin(2 * np.pi * f4 * t + p4)
    wake_wave_1 = A*2 * np.exp(-alpha * c * t) * \
        np.sin(2 * np.pi * f * t + phi)
    # wake_wave_2 = A*1.5 * np.exp(-alpha * c * t) * \
    #     np.sin(2 * np.pi * f * t + -0.226*phi)
    # wake_wave_4 = A*0.5 * np.exp(-alpha * c * t) * \
    #     np.sin(2 * np.pi * f * t + 0.226*phi)

    # Apply piecewise condition
    wave2_accel1 = np.where((t >= 0) & (t < 15), wake_wave_1, 0)
    # wave2_accel2 = np.where((t >= 7) & (t < 40), wake_wave_2, 0)
    # wave2_accel3 = wave2_accel1
    # wave2_accel4 = np.where((t >= 7) & (t < 40), wake_wave_4, 0)

    accel1 = wave2_accel1
    fourier_transform = np.fft.fft(accel1)
    # accel2 = wave1_accel2 + wave2_accel2
    # accel3 = wave1_accel3 + wave2_accel3
    # accel4 = wave1_accel4 + wave2_accel4
    return fourier_transform  # training was done in the frequency domain


def preprocess_data(raw_data):
    raw_data_array = np.array(raw_data)
    if raw_data_array.shape[0] != 4 and raw_data_array.shape[1] == 4:
        raw_data_array = raw_data_array.T
    averaged_data = raw_data_array.mean(axis=1)
    return averaged_data


# def confirm_with_satellite(image_path):
#     # this should come from satellite
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

#     image_np = np.array(image)

#     # Actual detection
#     input_tensor = tf.convert_to_tensor(
#         np.expand_dims(image_np, 0), dtype=tf.float32)
#     detections = detection_model(input_tensor)

#     if detections.get('num_detections') > 0:
#         return True
#     else:
#         return False


@app.route('/detect', methods=['GET'])
def detect_ship():
    raw_data = retrieve_data_from_accelerometer()

    data_for_prediction = preprocess_data(raw_data)

    prediction = model.predict([data_for_prediction])
    if prediction[0] in ships:
        # Check confidence level (if your model provides probabilities)
        # Assuming the model.predict_proba method is available and used here
        confidence = max(model.predict_proba([data_for_prediction])[0])

        if confidence < 0.8:  # Assuming 80% confidence threshold
            # This should be provided by the client or be a static path
            # image_path = '/Users/owebb/defense-tech-hackathon/satelite_images/sat1.jpg'
            # confirmation = confirm_with_satellite(image_path)
            # if confirmation:
            #     c.execute("INSERT INTO ship_detections (timestamp, ship_type, confidence, image_path) VALUES (datetime('now'), ?, ?, ?)",
            #               (prediction[0], confidence, image_path))
            #     conn.commit()
            #     alarm_message = "SOUNDING ALARM VIA LTE TO MAINLAND"
            # else:
            #     c.execute("INSERT INTO ship_detections (timestamp, ship_type, confidence, image_path) VALUES (datetime('now'), ?, ?, ?)",
            #               (prediction[0], confidence, image_path))
            #     conn.commit()
            alarm_message = "Detection not confirmed by satellite"
        else:
            alarm_message = "High confidence detection, alarm sounded"

        return jsonify({
            'prediction': prediction[0],
            'confidence': confidence,
            'alarm_message': alarm_message
        })
    else:
        return jsonify({'message': 'No ship detected'})


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
