

def alter_operation(conversation, parse_text, i, **kwargs):
    features = conversation.get_var('features').contents
    feature_name = parse_text[i+1]
    value = parse_text[i+2]

    features[feature_name] = float(value)
    return_string = f"Feature {feature_name} changed to {value}"
    return_string += "<br>"
    return_string += "All changes:"
    definitions = conversation.feature_definitions
    keys = list(definitions.keys())
    for key in keys:
        if key in features:
            return_string += "<br>"
            return_string += f"{key} = {features[key]}"
    conversation.add_var('features', features, 'features')
    print(features)
    return return_string, 1
