from flask import Flask, render_template, request

# from tensorflow import keras
import tensorflow as tf

from keras.preprocessing.image import load_img
load_img = tf.keras.preprocessing.image.load_img
from keras.preprocessing.image import img_to_array
from keras.application.vgg16 import preprocess_input
from keras.application.vgg16 import decode_predictions
# from keras.application.vgg16 import VGG16
# VG16 works but because deployed on heroku, i had limited space.
from keras.application.resnet50 import ResNet50



app = Flask(__name__)
# model = VGG16()
# model = ResNet50()
model = keras.application.ResNet50()

@app.route('/', methods=['GET'])
def helloworld():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def predict():
    imagefile=request.files['imagefilename']
    image_path = "./images/" + imagefile.filename
    imagefile.save(image_path)

    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape(1, image.shape[0], image.shape[1], image.shape[2])
    image = preprocess_input (image)
    yhat = model.predict(image)
    label = decode_predictions(yhat)
    label = label[0][0]

    classification = '%s (%.2f%%)' % (label[1], label[2] * 100)
    
    return render_template('index.html', prediction=classification)

if __name__ == '__main__':
    app.run(port=3000, debug=True)