"""
Add new label to prediction df
"""
import pandas as pd
import json
import format_predictions as fp


comparison_sheet_file = 'data/prediction_comparison_doc_number.csv'
prediction_file = 'data/local_predictions_document_number.json'
output_file = 'data/file_comparison_document_number.csv'
model_id = 'csc_annotation'

predictions = fp.read_predictions(prediction_file, model_id)
labeled_text_dict = fp.get_labels_from_predictions(predictions)

document_numbers_df = fp.post_process_recording_date(labeled_text_dict, key='Document Number')

document_numbers_df.index.name = 'Filename'
document_numbers_df.reset_index(inplace=True)
document_numbers_df['Filename'] = document_numbers_df['Filename'].str.replace('pdf', 'tif')
document_numbers_df.set_index('Filename', inplace=True)
comparison_df = pd.read_csv(comparison_sheet_file).iloc[0: 50]
comparison_df.set_index('Filename', inplace=True)

final_df = pd.concat([comparison_df, document_numbers_df], axis=1)
final_df.reset_index().to_csv(output_file, index=False)
print("finished")
