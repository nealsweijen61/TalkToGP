from explain.actions.utils import get_models
from explain.actions.ops import get_expr_operation

def simplify_operation(conversation, parse_text, i, **kwargs):
    models = get_models(conversation)
    return_string = ""
    return_string += "The model(s) have been simplified <br><br>"
    for model in models:
        model.getSimplify()

    s, i = get_expr_operation(conversation, parse_text, i , **kwargs)
    return_string += s
    return return_string, i