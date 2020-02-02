"""
Script to create plain text files from csv file generted by BlueJet
"""

import pandas as pd
import os


data_file = 'data/data_set_test.csv'
outdir = 'data/plaintext_test_files'
data_df = pd.read_csv(data_file)

for index, row in data_df.iterrows():
    filename = row.filepath.split('.')[0] + '.txt'
    output_path = os.path.join(outdir, filename)
    text = row.text
    with open(output_path, 'w') as f:
        f.write(text)
