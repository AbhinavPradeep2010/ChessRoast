import math


def eval_to_win_probability(eval_cp):
    eval_cp = max(-10000, min(10000, eval_cp))
    return 100/ (1 + math.exp(-0.004 * eval_cp))


def eval_to_cp(eval_value):

    if isinstance(eval_value, str) and "M" in eval_value:

        if eval_value.startswith("-"):
            return -10000

        return 10000

    return eval_value


def classify_move(org_cp, new_cp, turn, book=False):

    org_cp = eval_to_cp(org_cp)
    new_cp = eval_to_cp(new_cp)

    if turn == "white":
        probability_swing = eval_to_win_probability(org_cp) - eval_to_win_probability(new_cp)
    else:
        probability_swing = eval_to_win_probability(new_cp) - eval_to_win_probability(org_cp)

    probability_swing = max(0, probability_swing)
        
    classification = ""

    if probability_swing <= 1:
        classification = "best"
    elif probability_swing <= 2:
        classification = "excellent"
    elif probability_swing <= 4:
        classification = "good"
    elif probability_swing <= 9:
        classification = "inaccuracy"
    elif probability_swing <= 15:
        classification = "mistake"
    else:
        classification = "blunder"
    return {
        "classification": classification,
        "probability_swing": round(probability_swing, 2)
    }