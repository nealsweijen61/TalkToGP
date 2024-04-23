from data.customClassifier import CustomClassifier
from explain.actions.utils import get_models
import numpy as np

def outlier_operation(conversation, parse_text, i, **kwargs):
    models = get_models(conversation)
    data = conversation.temp_dataset.contents['X']
    if len(conversation.temp_dataset.contents['X']) == 0:
        # In the case that filtering has removed all the instances
        return 'There are no instances that meet this description!', 0
    labels = conversation.temp_dataset.contents['y']
    return_string = ""
    threshold = 1000
    bad_predictions_count = {}
    all_errors = []
    thresholds = []
    percentile = 99
    if parse_text[i+1].isnumeric():
        percentile = int(parse_text[i+1])
    print(percentile)
    for model in models:
        predictions = model.predict(data)
        errors = abs(predictions - labels)
        all_errors.extend(errors)
        # Determine threshold based on percentile of errors
        thresholds.append(np.percentile(errors, percentile))

    print("thresh:", thresholds)
    return_string = ""
    for i, model in enumerate(models):
        # Make predictions
        predictions = model.predict(data)
        # Calculate error (e.g., Mean Absolute Error)
        errors = abs(predictions - labels)
        # Identify bad predictions
        bad_predictions = errors > thresholds[i]
        # print("pred", bad_predictions)
        # Count bad predictions
        bad_indices = np.where(errors > thresholds[i])[0]
        bad_ids = data.iloc[bad_indices]
        ids = list(bad_ids.index)
        ids.sort()
        print("bad ids", type(ids), ids)
        bad_predictions_count[model.id] = sum(bad_predictions)
        return_string += f"for model {model.id} it predicts the following {bad_predictions_count[model.id]} ids the worst:"
        return_string += f"{','.join(map(str, ids))} <br>"
    print(bad_predictions_count)
    return return_string, 1