import pandas as pd
import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
from pathlib import Path
from foodclassification.entity.config_entity import (TrainingConfig)

class PlotLosses(tf.keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        self.fig = plt.figure()
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.i += 1

class Training:
    #training_dataframe = pd.read_csv('artifacts/data_ingestion/train_img.csv')

    def __init__(self, config: TrainingConfig):
        self.config = config


    def batch_generator(self, batch_size, gen_x):
        batch_features = np.zeros((batch_size,256,256,3))
        batch_labels = np.zeros((batch_size,61))
        while True:
            for i in range(batch_size):
                batch_features[i], batch_labels[i] = next(gen_x)
            yield batch_features, batch_labels

    def generate_data(self, filelist, img_path, target):
        while True:
            for i,j in enumerate(filelist):
                X_train = cv2.imread(img_path + j, cv2.IMREAD_COLOR)
                X_train = cv2.resize(X_train, (256,256), interpolation= cv2.INTER_LINEAR)

                y_train = target[i]

                yield X_train, y_train

    def create_model(self):
        base_model = tf.keras.applications.EfficientNetB1(
            weights= "imagenet", include_top=False, input_shape=(256,256,3)
        )
        num_classes=61

        x = base_model.output
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        predictions = tf.keras.layers.Dense(num_classes, activation= 'softmax')(x)
        model = tf.keras.Model(inputs = base_model.input, outputs = predictions)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss="categorical_crossentropy", metrics=['acc'])
        return model
    
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    def train(self):
        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.1, patience=1, verbose=1, mode='min',
            min_delta=0.0001, cooldown=2, min_lr=0)
        
        training_dataframe = pd.read_csv(self.config.trains_img_csv)
        y_dev = np.asarray(pd.get_dummies(training_dataframe["ClassName"]))
        X_dev = np.asanyarray(training_dataframe["ImageId"])
        train_path = "artifacts/data_ingestion/train_images/train_images/"
        batch_size = self.config.params_batch_size
        num_epoch = self.config.params_epochs
        plot_losses = PlotLosses()
        model = self.create_model()
        history = model.fit(x=self.batch_generator(batch_size, self.generate_data(X_dev, train_path, y_dev)), epochs=num_epoch,
                            steps_per_epoch=int(y_dev.shape[0]/batch_size), verbose = 1, callbacks = [plot_losses,reduce_lr] )
        
        self.save_model(path=self.config.trained_model_path, model=model)