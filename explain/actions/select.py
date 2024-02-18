
import pandas as pd

def get_operation_value(feature_name, model):
    if feature_name == 'selectoperators':
        return get_operation_value(feature_name, model)
    elif feature_name ==  'selectnodes':
        return model.numNodes()
    elif feature_name == 'selectconstants':
        return model.numConstants()
    elif feature_name == 'selectfeatures':
        return model.numFeatures()
    elif feature_name == 'selectacurracy':
        return model.getAccuracy()
    elif feature_name == 'selectcomplex':
        return model.getComplexity()
    else:
        raise NameError(f"Parsed unkown feature name {feature_name}")

def numerical_filter(parse_text, temp_select, i, feature_name):
    """Performs numerical filtering.

    All this routine does (though it looks a bit clunky) is look at
    the parse_text and decide which filtering operation to do (e.g.,
    greater than, equal to, etc.) and then performs the operation.
    """
    # Greater than or equal to
    if parse_text[i+2] == 'greater' and parse_text[i+3] == 'equal':
        feature_value = float(parse_text[i+5])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model) >= feature_value]
    # Greater than
    elif parse_text[i+2] == 'greater':
        feature_value = float(parse_text[i+4])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model) > feature_value]
        print("WORKING:", updated_dset)
    # Less than or equal to
    elif parse_text[i+2] == 'less' and parse_text[i+3] == 'equal':
        feature_value = float(parse_text[i+5])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model) <= feature_value]
    # Less than
    elif parse_text[i+2] == 'less':
        feature_value = float(parse_text[i+4])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model) < feature_value]
    # Equal to
    elif parse_text[i+2] == 'equal':
        feature_value = float(parse_text[i+4])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model) == feature_value]
    # Not equal to
    elif parse_text[i+2] == 'not':
        feature_value = float(parse_text[i+5])
        updated_dset = [model for model in temp_select if get_operation_value(feature_name, model) != feature_value]
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
    if is_or:
        # construct a new temp data set to or with
        temp_select = conversation.build_temp_select(save=False).contents
    else:
        temp_select = conversation.temp_select.contents

    operation = parse_text[i]
    feature_name = parse_text[i+1]
    print("FEATURENAME", feature_name)
    if feature_name == 'selectoperators' or feature_name =='selectnodes' or feature_name =='selectconstants' or feature_name =='selectfeatures' or feature_name =='selectacurracy' or feature_name =='selectcomplex':
        updated_dset = numerical_filter(parse_text, temp_select, i, feature_name)
    elif feature_name == 'model':
        feature_value = int(parse_text[i+2])
        updated_dset = [temp_select[feature_value]]
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

    return '', 1