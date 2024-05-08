"""Sample a prompt for a specific action."""
import numpy as np
import random
import os
from os.path import exists
from explain.prompts import get_user_part_of_prompt

ACTION_2_FILENAME = {
    "self": None,
    "score": "prompts/questions/score.txt",
    "likelihood": "likelihood_prompts.txt",
    "important": "prompts/questions/important.txt",
    "explain": "explanation_prompts.txt",
    "predict": "prompts/questions/predict.txt",
    "whatif": "whatif_prompts.txt",
    "cfe": "cfe_prompts.txt",
    "function": None,
    "show": "prompts/questions/show.txt",
    "description": "prompts/questions/dataset.txt",
    "interactions": "interactions.txt",
    "mistake": "prompts/questions/mistakes.txt",
    "labels": "prompts/questions/labels.txt",
    "select" : "prompts/questions/select.txt",
    "tree": "prompts/questions/treemod.txt",
    "plotTree": "prompts/questions/plottree.txt",
    "GP": "prompts/questions/gpinfo.txt",
    "common": "prompts/questions/common.txt",
    "simplify": "prompts/questions/simplify.txt",
    "GPshow": "prompts/questions/gpshow.txt"
}


def replace_non_existent_id_with_real_id(prompt: str, real_ids: list[int]) -> str:
    """Attempts to replace ids that don't exist in the data with ones that do.

    The problem is that prompt generation may create prompts with ids that don't occur
    in the data. This is fine for the purposes of generating training data. However,
    when the user clicks "generate an example question" we should try and make sure
    that the example question uses ids that actually occur in the data, so they
    don't get errors if they try and run the prompt (this seems a bit unsatisfying).
    This function resolves this issues by trying to find occurrences of ids in the prompts
    and replaces them with ids that are known to occur in the data.

    Arguments:
        prompt: The prompt to try and replace with an actual id in the data.
        real_ids: A list of ids that occur in the data **in actuality**
    Returns:
        resolved_prompt: The prompt with ids replaced
    """
    split_prompt = prompt.split()
    for i in range(len(split_prompt)):
        if split_prompt[i] in ["point", "id", "number", "for", "instance"]:
            if i+1 < len(split_prompt):
                # Second option is for sentence end punctuation case
                if split_prompt[i+1].isnumeric() or split_prompt[i+1][:-1].isnumeric():
                    split_prompt[i+1] = str(np.random.choice(real_ids))
    output = " ".join(split_prompt)
    return output


def sample_prompt_for_action(action: str,
                             filename_to_prompt_ids: dict,
                             prompt_set: dict,
                             real_ids: list[int]) -> str:
    """Samples a prompt for a specific action.

    Arguments:
        real_ids: A list of naturally occurring **data point** ids.
        prompt_set: The full prompt set. This is a dictionary that maps from **prompt** ids
                    to info about the prompt.
        action: The action to sample a prompt for
        filename_to_prompt_ids: a map from the prompt filenames to the id of a prompt.
                                Note, in this context, 'id' refers to the 'id' assigned
                                to each prompt and *not* an id of a data point.
    Returns:
        prompt: The sampled prompt
    """
    print("filename_ids", filename_to_prompt_ids)
    print("prompt set", prompt_set)
    if action == "self":
        return "Could you tell me a bit more about what this is?"
    elif action == "function":
        return "What can you do?"
    elif action == "pareto":
        return "Show the pareto front"
    elif action == "GP" or action == "select" or action == "important" or action == "description" or action == "show" or action == "score" or action == "labels" or action == "predict" or action == "tree" or action == "plotTree" or action == "common" or action == "simplify" or action == "GPshow" or action == "mistake":
        return choosePrompt(ACTION_2_FILENAME[action])

    
    elif action in ACTION_2_FILENAME:
        filename_end = ACTION_2_FILENAME[action]
        for filename in filename_to_prompt_ids:
            if filename.endswith(filename_end):
                prompt_ids = filename_to_prompt_ids[filename]
                chosen_id = np.random.choice(prompt_ids)
                i = 0
                # Try to not return prompts that are not complete
                # for the particular dataset (i.e., those that have
                # a wildcard still in them with "{" )
                prompt = prompt_set[chosen_id]["prompts"][0]
                user_part = get_user_part_of_prompt(prompt)
                while "{" in user_part or i < 100:
                    chosen_id = np.random.choice(prompt_ids)
                    i += 1
                    prompt = prompt_set[chosen_id]["prompts"][0]
                    user_part = get_user_part_of_prompt(prompt)
                final_user_part = replace_non_existent_id_with_real_id(user_part, real_ids)
                return final_user_part
        message = f"Unable to filename ending in {filename_end}!"
        raise NameError(message)
    else:
        message = f"Unknown action {action}"
        raise NameError(message)

def choosePrompt(filename):
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script
    file_path = os.path.join(script_dir, filename) 
    print(file_path)
    print(exists(file_path))
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip()  # strip() removes any trailing newline characters
