"""
Handle post processing for prediction outputs and write out to excel file
"""
import json
from collections import defaultdict
import pandas as pd


def read_predictions(prediction_file, model_id):
    with open(prediction_file) as f:
        json_obj = json.load(f)
    return json_obj[model_id]['predictions']


def get_labels_from_predictions(predictions, threshold=0.1):
    full_results = {}
    for filename, pred in predictions.items():
        results = defaultdict(list)
        for annotation in pred:
            label = annotation['label']
            confidence = annotation['confidence'][label]
            text = annotation['text'].strip()
            if confidence > threshold:
                results[label].append((text, confidence))
        full_results[filename] = results
    return full_results


def post_process_recording_date(labeled_text_dict, key='Recording Date'):
    recording_date_dict = {}
    predicted_lbl = key + ' Predicted'
    confidence_lbl = key + ' Confidence'
    for filename, labels in labeled_text_dict.items():
        recording_date_list = labels.get(key, None)
        if recording_date_list:
            recording_date = max(recording_date_list, key=lambda x: x[1])
            result = {
                predicted_lbl: recording_date[0],
                confidence_lbl: recording_date[1]
                }
            recording_date_dict[filename] = result
    recording_date_df = (
        pd.DataFrame.from_dict(recording_date_dict, orient='index')
        )
    return recording_date_df


def post_process_names(labeled_text_dict, key):
    name_dict = {}
    predicted_lbl = key + ' Predicted'
    confidence_lbl = key + ' Confidence'
    for filename, labels in labeled_text_dict.items():
        name_list = labels.get(key, None)
        if name_list:
            name = ' '.join([x[0] for x in name_list]).replace('\n', '')
            confidence = [x[1] for x in name_list]
            result = {
                predicted_lbl: name,
                confidence_lbl: confidence if len(confidence) > 1 else confidence[0]
            }
            name_dict[filename] = result
    name_df = pd.DataFrame.from_dict(name_dict, orient='index')
    return name_df


if __name__ == '__main__':
   
    prediction_file = 'data/local_predictions.json'
    answer_key_file = 'data/answer_key_indico_generated.csv'
    output_file = 'data/prediction_comparison.csv'
    model_id = 'csc_annotation'

    predictions = read_predictions(prediction_file, model_id)
    labeled_text_dict = get_labels_from_predictions(predictions)

    recording_date_df = post_process_recording_date(labeled_text_dict)
    borrower_name_df = post_process_names(labeled_text_dict, 'Borrower Name')
    lender_name_df = post_process_names(labeled_text_dict, 'Lender Name')
    mailing_address_df = post_process_names(labeled_text_dict, 'Mailing Address')
    property_address_df = post_process_names(labeled_text_dict, 'Property Address')
    document_number_df = post_process_recording_date(labeled_text_dict, 'Document Number')
    predictions_df = pd.concat([
        recording_date_df,
        borrower_name_df,
        lender_name_df,
        mailing_address_df,
        property_address_df,
        document_number_df,
        ], axis=1)
    predictions_df.index.name = 'Filename'

    answer_key_df = pd.read_csv(answer_key_file).set_index('Filename')    
    final_output = pd.concat([answer_key_df, predictions_df], axis=1)

    columns = [
        'Recording Date',
        'Recording Date Predicted',
        'Recording Date Confidence',
        'Borrower Name',
        'Borrower Name Predicted',
        'Borrower Name Confidence',
        'Lender Name',
        'Lender Name Predicted',
        'Lender Name Confidence',
        'Mailing Address',
        'Mailing Address Predicted',
        'Mailing Address Confidence',
        'Property Address',
        'Property Address Predicted',
        'Property Address Confidence',
        'Document Number',
        'Document Number Predicted',
        'Document Number Confidence',
        ]
    final_output[columns].to_csv(output_file)
    print('finished')
