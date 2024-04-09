"""Functions used as jobs"""


from typing import Iterable
from operator import itemgetter
from collections import OrderedDict
from app.data_ingestor import DataIngestor

class Job:
    """Structure for job related information"""
    def __init__(self, func : callable, id : int, data : DataIngestor, *args):
        self.func = func
        self.id = id
        self.data = data
        self.args = args


def without_nan(d : dict):
    """Remove entrie that don'y have stratification"""
    return {k: v for k, v in d.items() if k != ''}


def data_values(data : dict) -> Iterable[float]:
    """Get values only from nested dictionary"""
    for v in data.values():
        if isinstance(v, dict):
            yield from data_values(v)
        elif isinstance(v, list):
            yield from v
        else:
            yield v


def _states_mean_func(question : str, data : DataIngestor) -> list:
    """Aux to calculate all states mean"""
    data_states = data.data[question]

    return sorted([(state, _state_mean_func(question, state, data))
                   for state in data_states.keys()], key=itemgetter(1))


def states_mean_func(question : str, data : DataIngestor) -> OrderedDict:
    """Calculates all states mean and returns the result in a sorted dict"""
    return OrderedDict(_states_mean_func(question, data))


def _state_mean_func(question : str, state : str, data : DataIngestor) -> float:
    """Aux to calculate state mean"""
    data_strats = data.data[question][state]
    values = list(data_values(data_strats))

    return sum(values) / len(values)


def state_mean_func(question : str, state : str, data : DataIngestor) -> dict:
    """Calculates state mean and returns the result as a dictionary"""
    return {state: _state_mean_func(question, state, data)}


def best5_func(question : str, data : DataIngestor) -> OrderedDict:
    """Calculates best 5 states and returns the result as a sorted dict"""
    if question in data.questions_best_is_min:
        return OrderedDict(_states_mean_func(question, data)[:5])

    return OrderedDict(reversed(_states_mean_func(question, data)[-5:]))


def worst5_func(question : str, data : DataIngestor) -> OrderedDict:
    """Calculates worst 5 states and returns the result as a sorted dict"""
    if question in data.questions_best_is_max:
        return OrderedDict(_states_mean_func(question, data)[:5])

    return OrderedDict(reversed(_states_mean_func(question, data)[-5:]))


def _global_mean_func(question : str, data : DataIngestor) -> float:
    """Aux to calculate the global mean"""
    data_states = data.data[question]
    values = list(data_values(data_states))

    return sum(values) / len(values)


def global_mean_func(question : str, data : DataIngestor) -> dict:
    """Calculates global mean and returns the result as a dictionary"""
    return {"global_mean": _global_mean_func(question, data)}


def diff_from_mean_func(question : str, data : DataIngestor) -> dict:
    """Calculates the diff from mean for all states and returns the result as a dictionary"""
    data_states = data.data[question]

    return {state: _state_diff_from_mean_func(question, state, data)
            for state in data_states.keys()}


def _state_diff_from_mean_func(question : str, state : str, data : DataIngestor) -> float:
    """Aux to calculate state diff from mean"""
    global_mean = _global_mean_func(question, data)
    state_mean = _state_mean_func(question, state, data)

    return global_mean - state_mean


def state_diff_from_mean_func(question : str, state : str, data : DataIngestor) -> dict:
    """Calculates state diff from mean and returns the result as a dictionary"""
    return {state: _state_diff_from_mean_func(question, state, data)}


def mean_by_category_func(question : str, data : DataIngestor) -> dict:
    """Calculates mean by category for every state and returns the result as a dictionary"""
    data_states = data.data[question]

    values = {}
    for state in data_states.keys():
        state_values = _state_mean_by_category_func(question, state, data)

        for strat_cat, strat, value in state_values:
            values[f'(\'{state}\', \'{strat_cat}\', \'{strat}\')'] = value

    return values


def _state_mean_by_category_func(question : str, state : str, data : dict) -> list:
    """Aux to calculate state mean by category"""
    data_without_nan = without_nan(data.data[question][state])

    values = []
    for strat_cat in data_without_nan.keys():
        for strat in data_without_nan[strat_cat].keys():
            values_list = data_without_nan[strat_cat][strat]
            values.append((strat_cat, strat, sum(values_list) / len(values_list)))

    return values


def state_mean_by_category_func(question : str, state : str, data : dict) -> dict:
    """Calculate state mean by category for state and returns the result as a dictionary"""
    values = _state_mean_by_category_func(question, state, data)

    return {state: {f'(\'{strat_cat}\', \'{strat}\')': val for (strat_cat, strat, val) in values}}
