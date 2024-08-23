
# this will take the image and predict the results
from keras.models import load_model
#from keras.utils.layer_utils import print_summary
#from tensorflow.keras.utils import print_summary
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.applications.vgg19 import preprocess_input
import json
import os
import pandas as pd
import time

baseDir = os.path.join(os.getcwd(), 'trained_model')

print("loading modle here")
model = load_model(os.path.join(baseDir, 'best_model.h5'))



data = json.load(open(os.path.join(baseDir, 'datafile.json')))
databaseDir = os.path.join(os.getcwd(), 'data_files')
df = pd.read_csv(open(os.path.join(databaseDir, "supplement_info.csv")))
# print("DataFrame : "  )
# print(df)

def prediction(path):
    try:
        img = load_img(path, target_size=(256, 256))
        i = img_to_array(img)
        im = preprocess_input(i)
        img = np.expand_dims(im, axis=0)
    except Exception as e:
        print(f"Invalid image: {e}")
        return None

    try:
        start_time = time.time()
        pred = np.argmax(model.predict(img))
        end_time = time.time()
        value = data[str(pred)]

        print(f"The image belongs to {value}")
        print("The processing time is ", end_time - start_time)
        
        matching_rows = df.loc[df['disease_name'] == value]
        if matching_rows.empty:
            print("No matching disease found in the dataset.")
            return None
        
        return matching_rows.values[0][0]
    
    except KeyError as e:
        print(f"Prediction key error: {e}")
        return None


def getDataFromCSV(index):
    if df.shape[0] > index:
        return df.loc[df['index'] == index].values[0]
    else :
        return []



if __name__ == "__main__":
    # just for the testing
    path = os.path.join(baseDir, "baseimg.png")
    result, processing_time = prediction(path)
    print(f"Processing time: {processing_time:.4f} seconds")
    print(prediction(path))
