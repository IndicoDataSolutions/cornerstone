"""
Compute predictions after model has been trained
"""
from indicoio.custom import FinetuneCollection
import indicoio

from BlueJet.predictions import Prediction
import pandas as pd
import os


if __name__ == '__main__':
    # set api_key to use indico pdf extractor
    indicoio.config.api_key = os.environ.get('CORNERSTONE_API_KEY')

    test_data_file = '/data/data_set_test.csv'
    output_path = 'data/local_predictions.json'

    model_id = '4041_23414_1579799204'

    df = pd.read_csv(test_data_file)
    text_data = df['text'].tolist()
    filepath_id = df['filepath'].tolist()

    print('predictions started')
    model_dict = {
        'csc_annotation': FinetuneCollection(model_id)
    }
    predictor = Prediction(model_dict)
    predictions = predictor.predict(
        text_data,
        ids=filepath_id,
        batch_size=10,
        local_batching=True
    )
    predictor.to_file(output_path)
    print("predictions saved to {}".format(output_path))
