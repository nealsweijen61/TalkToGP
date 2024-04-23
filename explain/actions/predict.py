"""Prediction operation."""
import numpy as np
from explain.actions.utils import get_models
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from explain.actions.utils import gen_parse_op_text, get_parse_filter_text
import sys
import time

def predict_histogram(conversation, parse_text, i, **kwargs):
    models = get_models(conversation)
    
    data = conversation.temp_dataset.contents['X']

    if len(conversation.temp_dataset.contents['X']) == 0:
        return 'There are no instances that meet this description!', 0
    
    pred = models[0].predict(data)
    return_s = "s"

    return 

def predict_operation(conversation, parse_text, i, max_num_preds_to_print=1, **kwargs):
    models = get_models(conversation)
    return_s = ""
    i = 1

    data = conversation.temp_dataset.contents['X']

    if len(conversation.temp_dataset.contents['X']) == 0:
        return 'There are no instances that meet this description!', 0

    print("data size:", len(data))
    model_predictions = []
    totalMin = sys.maxsize
    totalMax = -sys.maxsize
    for model in models:
        model_prediction = model.predict(data)
        print("model epressionsw:", model.expr)
        curMax = max(model_prediction)
        curMin = min(model_prediction)
        if curMax > totalMax:
            totalMax = curMax
        if curMin < totalMin:
            totalMin = curMin
        model_predictions.append(model_prediction)

    for counter, model in enumerate(models):
        s, num = predict_operation2(conversation, model, parse_text, i, model_predictions[counter], totalMin, totalMax, max_num_preds_to_print, counter, **kwargs)
        return_s += s
        i *= num
    return return_s, i

def predict_operation2(conversation, model, parse_text, i, model_predictions, min, max, max_num_preds_to_print=1, counter = 0, **kwargs):
    """The prediction operation."""
    # model = conversation.get_var('model').contents
    # Format return string
    return_s = ""

    filter_string = gen_parse_op_text(conversation)

    if len(model_predictions) == 1:
        if counter == 0:
            return_s += "The true prediction is "
            return_s += f"<b>{conversation.temp_dataset.contents['y'].values[0]}</b> <br>"
        return_s += f"The instance with <b>{filter_string}</b> is predicted "
        if conversation.class_names is None:
            prediction_class = str(model_predictions[0])
            return_s += f"<b>{prediction_class}</b>"
        else:
            class_text = conversation.class_names[model_predictions[0]]
            return_s += f"<b>{class_text}</b>."
    else:
        intro_text = get_parse_filter_text(conversation)
        return_s += f"{intro_text} the model predicts:"
        # Create histogram
        if counter == 0:
            return_s += f"True output"
            trueOutput = conversation.temp_dataset.contents['y']
            return_s += createHistogram(trueOutput, counter-1, max, min)
        return_s += createHistogram(model_predictions, counter, max, min)

        # unique_preds = np.unique(model_predictions)
        # return_s += "<ul>"
        # for j, uniq_p in enumerate(unique_preds):
        #     return_s += "<li>"
        #     freq = np.sum(uniq_p == model_predictions) / len(model_predictions)
        #     round_freq = str(round(freq * 100, conversation.rounding_precision))

        #     if conversation.class_names is None:
        #         return_s += f"<b>class {uniq_p}</b>, {round_freq}%"
        #     else:
        #         class_text = conversation.class_names[uniq_p]
        #         return_s += f"<b>{class_text}</b>, {round_freq}%"
        #     return_s += "</li>"
        # return_s += "</ul>"
    return_s += "<br>"
    return return_s, 1


def createHistogram(model_predictions, counter, max, min):
    fig, ax = plt.subplots()
        
    data_range = max - min
    bin_width = data_range / 20
    # Create bins
    print("bins", min, max, bin_width)
    bins = np.arange(min, max + bin_width, bin_width)
    plt.hist(model_predictions, bins=bins, edgecolor='black')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    if counter >= 0:
        plt.title(f'Histogram of Model {counter+1}')
    else:
        plt.title(f"Histogram of true outputs")

    # Save plot to a temporary file
    timestamp = int(time.time())
    img_path = f'static/images/histo{counter}{timestamp}.png'
    plt.savefig(img_path)
    plt.close()
    return f'<img src="{img_path}" alt="drawing" width="400"/>'
