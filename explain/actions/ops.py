def ops_operation(conversation, parse_text, i, **kwargs):
    """Gives the number of operations"""
    # get the max value
    model = conversation.get_var('model').contents
    number = model.operators()
    # compose the return string
    return_string = f"The number of operators is {number}"
    # return the string and 1, indicating success
    return return_string, 1