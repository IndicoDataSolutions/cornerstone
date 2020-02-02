"""
This file handles the initial data setup for the POC

Steps include:
1) Convert .tif files to .pdf
2) Convert pdf files to plain text csv file
3) Split data into training and test set
"""
from BlueJet.filesystem import FileNavigator
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import indicoio


def convert_to_plaintext(data_path,
                         output_path,
                         convert=False,
                         **kwargs):
    """
    Convert files in data_path to a df of plaintext
    if convert == True, assume files in data_path are .tif files and convert
    to .pdf files first
    """

    if convert:
        navigator = FileNavigator(data_path, ["tif"])
        navigator.convert_to_pdf()

    navigator = FileNavigator(data_path, ["pdf"])
    navigator.generate_text_csv(output_path, **kwargs)


def split_test_train_set(output_path, **kwargs):
    """
    Split plaintext csv file into a test
    Acceptable kwargs are all kwargs used in train_test_split from sklearn
    """
    df = pd.read_csv(output_path)

    train, test = train_test_split(df, **kwargs)
    outfile_no_ext = os.path.splitext(output_path)[0]
    test_filename = outfile_no_ext + '_test.csv'
    train_filename = outfile_no_ext + '_train.csv'

    train.to_csv(train_filename)
    test.to_csv(test_filename)


if __name__ == '__main__':
    # set api_key to use indico pdf extractor
    indicoio.config.api_key = os.environ.get('CORNERSTONE_API_KEY')

    data_path = "/data/"
    output_path = os.path.join(data_path, 'cornerstone_data_set.csv')

    convert_to_plaintext(data_path,
                         output_path,
                         convert=True,
                         batch_size=10,
                         filepath_ignore_levels=4,
                         granularity='document',
                         filetype='pdf',
                         include_filepath=True)

    split_test_train_set(output_path, test_size=0.2)
