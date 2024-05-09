
import pandas as pd
from sympy import symbols

def get_operation_value(feature_name, model, conversation):
    if feature_name == 'selectoperators':
        return model.numOperators()
    elif feature_name ==  'selectnodes':
        return model.numNodes()
    elif feature_name == 'selectconstants':
        return model.numConstants()
    elif feature_name == 'selectfeatures':
        return model.numFeatures()
    elif feature_name == 'selectaccuracy':
        data = conversation.temp_dataset.contents['X']
        y_true = conversation.temp_dataset.contents['y']
        y_pred = model.predict(data)
        score = conversation.describe.get_score_text(y_true,
                                                    y_pred,
                                                    "mse",
                                                    conversation.rounding_precision,
                                                    "",
                                                    True)
        return float(score)
    elif feature_name == 'selectcomplex':
        return model.getComplexity()
    else:
        raise NameError(f"Parsed unkown feature name {feature_name}")
    
def operator_to_symbol(operator):
    if operator == "+":
        return "ADD"
    elif operator == "-":
        return "SUB"
    elif operator == "*":
        return "MUL"
    elif operator == "/":
        return "DIV"
    elif operator == "sin":
        return "SIN"
    elif operator == "cos":
        return "COS"
    elif operator == "tan":
        return "TAN"
    elif operator == "log":
        return "LOG"
    else:
        raise NotImplementedError(f"This operator is not yet implemented {operator}")
    
def feature_to_name(variable_name, definitions):
    print("Varaialbe_name", variable_name)
    variable_number = int(str(variable_name)[1:])
    keys = list(definitions.keys())
    if 0 <= variable_number <= len(keys):
        return keys[variable_number]
    else:
        return None

def check_operator(operator, model):
    operators = model.getOperators()
    operator = symbols(operator_to_symbol(operator))
    for item in operators:
        print(item, type(item))
    print("operator list", operators, type(operators))
    print("check", operator, type(operator), operator in operators)
    return operator in operators

def check_feature(conversation, feature, model):
    features = model.getFeatures()
    definitions = conversation.feature_definitions
    features = [feature_to_name(feat, definitions) for feat in features]
    for item in features:
        print(item, type(item))
    print("feature list", features, type(feature))
    print("check", feature, type(feature), feature in features)
    return feature in features
    
def operation_filter(parse_text, temp_select, i, feature_name):
    operator = parse_text[i+2]
    updated_dset = [model for model in temp_select if check_operator(operator, model)]
    return updated_dset

def feature_filter(conversation, parse_text, temp_select, i, feature_name):
    feature = parse_text[i+2]
    updated_dset = [model for model in temp_select if check_feature(conversation, feature, model)]
    return updated_dset

def best_filter(conversation, parse_text, temp_select, i, feature_name):
    bestNumber = int(parse_text[i+2])
    print("compara", bestNumber, len(temp_select))
    bestNumber = min(bestNumber, len(temp_select))
    print("bestnum", bestNumber)
    scores = []
    for model in temp_select:
        scores.append(get_operation_value("selectaccuracy", model, conversation))
    sorted_scores = sorted(scores, reverse=False)
    top_5_scores = sorted_scores[:bestNumber]
    print("top5", top_5_scores)
    updated_dset = [model for model in temp_select if get_operation_value("selectaccuracy", model, conversation) in top_5_scores]
            
    return updated_dset


def numerical_filter(conversation, parse_text, temp_select, i, feature_name):
    """Performs numerical filtering.

    All this routine does (though it looks a bit clunky) is look at
    the parse_text and decide which filtering operation to do (e.g.,
    greater than, equal to, etc.) and then performs the operation.
    """
    # Greater than or equal to
    if parse_text[i+2] == 'greater' and parse_text[i+3] == 'equal':
        feature_value = float(parse_text[i+5])
        print("feature value", feature_value)
        print("operation value", get_operation_value(feature_name, temp_select[0], conversation))
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model, conversation) >= feature_value]
    # Greater than
    elif parse_text[i+2] == 'greater':
        feature_value = float(parse_text[i+4])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model, conversation) > feature_value]
        print("WORKING:", updated_dset)
    # Less than or equal to
    elif parse_text[i+2] == 'less' and parse_text[i+3] == 'equal':
        feature_value = float(parse_text[i+5])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model, conversation) <= feature_value]
    # Less than
    elif parse_text[i+2] == 'less':
        feature_value = float(parse_text[i+4])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model, conversation) < feature_value]
    # Equal to
    elif parse_text[i+2] == 'equal':
        feature_value = float(parse_text[i+4])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model, conversation) == feature_value]
    # Not equal to
    elif parse_text[i+2] == 'not':
        feature_value = float(parse_text[i+5])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model, conversation) != feature_value]
    else:
        raise NameError(f"Uh oh, looks like something is wrong with {parse_text}")
    return updated_dset



def select_operation(conversation, parse_text, i, is_or=False, **kwargs):
    """The filtering operation.

    This function performs filtering on a data set.
    It updates the temp_dataset attribute in the conversation
    object.

    Arguments:
        is_or:
        conversation: The conversation object.
        parse_text: The grammatical text string.
        i: The index of the parse_text that filtering is called.
    """
    conversation.build_temp_select()
    if is_or:
        # construct a new temp data set to or with
        temp_select = conversation.build_temp_select(save=True).contents
    else:
        if conversation.temp_select == None:
            conversation.build_temp_select()
        print("temp_select", conversation.temp_select.contents)
        temp_select = conversation.temp_select.contents

    operation = parse_text[i]
    feature_name = parse_text[i+1]
    print("FEATURENAME", feature_name)
    if feature_name == 'selectoperators' or feature_name =='selectnodes' or feature_name =='selectconstants' or feature_name =='selectfeatures' or feature_name =='selectaccuracy' or feature_name =='selectcomplex':
        updated_dset = numerical_filter(conversation, parse_text, temp_select, i, feature_name)
    elif feature_name == 'model':
        feature_value = parse_text[i+2]
        indices = []
        counter = 0
        while feature_value != "[E]" and feature_value.isdigit():
            feature_value = int(feature_value)
            indices.append(feature_value)
            counter += 1
            feature_value = parse_text[i+2+counter]
        updated_dset = [temp_select[i - 1] for i in indices]
    elif feature_name == "selectnames":
        updated_dset = feature_filter(conversation, parse_text, temp_select, i, feature_name)
    elif feature_name == "selectop":
        updated_dset = operation_filter(parse_text, temp_select, i, feature_name)
    elif feature_name == "all":
        conversation.build_temp_select()
        updated_dset = conversation.temp_select.contents
    elif feature_name == "selectbest":
        updated_dset = best_filter(conversation, parse_text, temp_select, i, feature_name)
    else:
        raise NameError(f"Parsed unkown feature name {feature_name}")

    if is_or:
        current_dataset = conversation.temp_select.contents
        updated_dse = pd.concat([updated_dset, current_dataset]).drop_duplicates()
        conversation.add_interpretable_parse_op("or")
    else:
        conversation.add_interpretable_parse_op("and")

    # conversation.add_interpretable_parse_op(interp_parse_text)
    print("Dataset", updated_dset)
    conversation.temp_select.contents = updated_dset

    return_string = f"Selected model(s): "
    for i, model in enumerate(updated_dset):
        if i > 0:
            return_string += ","
        return_string += f" {model.id+1}"
    return_string += "<br><br>"


    return return_string, 1