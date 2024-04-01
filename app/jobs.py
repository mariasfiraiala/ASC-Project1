from typing import Iterable
from operator import itemgetter
from data_ingestor import DataIngestor


class Job:
    def __init__(self, func : callable, id : int, *args):
        self.func = func
        self.id = id
        self.args = args


def data_values(data : dict) -> Iterable[float]:
    for v in data.values():
        if isinstance(v, dict):
            yield from data_values(v)
        elif isinstance(v, list):
            yield from v
        else:
            yield v


def states_mean_func(question : str, data : DataIngestor) -> list:
    data_states = data.data[question]

    return sorted([(state, state_mean_func(question, state, data)) for state in data_states.keys()], key=itemgetter(1))

 
def state_mean_func(question : str, state : str, data : DataIngestor) -> float:
    data_strats = data.data[question][state]
    values = list(data_values(data_strats))

    return sum(values) / len(values)


def best5_func(question : str, data : DataIngestor) -> list:
    if question in data.questions_best_is_min:
        return states_mean_func(question, data)[:5]

    return states_mean_func(question, data)[-5:]


def worst5_func(question : str, data : DataIngestor) -> list:
    if question in data.questions_best_is_max:
        return states_mean_func(question, data)[:5]

    return states_mean_func(question, data)[-5:]


def global_mean_func(question : str, data : DataIngestor) -> float:
    values = list(data_values(data.data))

    return sum(values) / len(values)


def diff_from_mean_func(question : str, data : DataIngestor) -> list:
    data_states = data.data[question]

    return sorted([(state, state_diff_from_mean_func(question, state, data)) for state in data_states.keys()], key=itemgetter(1), reverse=True)


def state_diff_from_mean_func(question : str, state : str, data : DataIngestor) -> float:
    global_mean = global_mean_func(question, data)
    state_mean = state_mean_func(question, state, data)

    return global_mean - state_mean
