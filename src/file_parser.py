import json
from pathlib import Path

from src.error import Error

def file_parser(file_name: str) -> dict:
    if not Path(file_name).is_file():
        Error.throw(Error.FAIL, Error.FILE_NOT_FOUND_ERROR, f"file not found: {file_name}")

    try:
        with open(file_name, 'r') as file:
            json_file: dict = json.loads(file.read())
    except UnicodeDecodeError:
        Error.throw(Error.FAIL, Error.UNICODE_DECODE_ERROR, f"'utf-8' codec can't decode byte")
    except PermissionError:
        Error.throw(Error.FAIL, Error.PERMISSION_ERROR, f"permission denied: {file_name}")
    except json.decoder.JSONDecodeError:
        Error.throw(Error.FAIL, Error.JSON_DECODE_ERROR, "JSON decode error")

    for check in [__general_check, __alphabet_check, __name_check, __blank_check, __states_check, __initial_check,
                  __finals_check, __transitions_check]:
        check(json_file)

    return json_file


def __is_empty(values) -> bool:
    return False in map(lambda value: True if value else False, values)


def __is_not_list(value) -> bool:
    return not isinstance(value, list)


def __is_not_dict(value) -> bool:
    return not isinstance(value, dict)


def __is_not_string(values) -> bool:
    return False in map(lambda value: isinstance(value, str), values)


def __is_repeated(values) -> bool:
    return True in map(lambda value: values.count(value) > 1, values)


def __is_not_size_one(values) -> bool:
    return True in map(lambda value: len(value) > 1, values)


def __is_not_in(values, target) -> bool:
    return False in map(lambda value: value in target, values)


def __general_check(json_file: dict):
    primary_keys: list[str] = ['name', 'alphabet', 'blank', 'states', 'initial', 'finals', 'transitions']

    if list(json_file.keys()) != primary_keys:
        Error.throw(Error.FAIL, Error.JSON_FORMAT_ERROR, f"primary keys has to be: {', '.join(primary_keys)}")
    elif __is_empty(json_file.values()):
        Error.throw(Error.FAIL, Error.EMPTY_FIELD_ERROR, "primary values can't be empty")


def __alphabet_check(json_file: dict):
    values: list[str] = json_file['alphabet']

    if __is_not_list(values):
        Error.throw(Error.FAIL, Error.TYPE_ERROR, "alphabet has to be contained in a list")
    elif __is_empty(values):
        Error.throw(Error.FAIL, Error.EMPTY_FIELD_ERROR, "alphabet can't be empty")
    elif __is_not_string(values):
        Error.throw(Error.FAIL, Error.TYPE_ERROR, "alphabet values have to be string")
    elif __is_repeated(values):
        Error.throw(Error.FAIL, Error.REPETITION_ERROR, "alphabet values have to be unique")
    elif __is_not_size_one(values):
        Error.throw(Error.FAIL, Error.REPETITION_ERROR, "alphabet values have to be size 1")


def __name_check(json_file: dict):
    if __is_not_string([json_file['name']]):
        Error.throw(Error.FAIL, Error.TYPE_ERROR, "name has to be a string")


def __blank_check(json_file: dict):
    value: str = json_file['blank']

    if __is_not_string([value]):
        Error.throw(Error.FAIL, Error.TYPE_ERROR, "blank character has to be a string")
    elif __is_not_in([value], json_file['alphabet']):
        Error.throw(Error.FAIL, Error.JSON_FORMAT_ERROR, f"blank character '{value}' should be part of the alphabet")


def __states_check(json_file: dict):
    values: list[str] = json_file['states']

    if __is_not_list(values):
        Error.throw(Error.FAIL, Error.TYPE_ERROR, "states have to be contained in a list")
    elif __is_empty(values):
        Error.throw(Error.FAIL, Error.EMPTY_FIELD_ERROR, "states can't be empty")
    elif __is_not_string(values):
        Error.throw(Error.FAIL, Error.TYPE_ERROR, "states values have to be string")
    elif __is_repeated(values):
        Error.throw(Error.FAIL, Error.REPETITION_ERROR, "states values have to be unique")


def __initial_check(json_file: dict):
    value: str = json_file['initial']

    if __is_not_string([value]):
        Error.throw(Error.FAIL, Error.TYPE_ERROR, "initial state has to be a string")
    elif __is_not_in([value], json_file['states']):
        Error.throw(Error.FAIL, Error.JSON_FORMAT_ERROR, f"initial state '{value}' should be one of states")


def __finals_check(json_file: dict):
    values: list[str] = json_file['finals']

    if __is_not_list(values):
        Error.throw(Error.FAIL, Error.TYPE_ERROR, "final states have to be contained in a list")
    elif __is_not_string(values):
        Error.throw(Error.FAIL, Error.TYPE_ERROR, "final states have to be string")
    elif __is_repeated(values):
        Error.throw(Error.FAIL, Error.REPETITION_ERROR, "final states have to be unique")
    elif __is_not_in(values, json_file['states']):
        Error.throw(Error.FAIL, Error.JSON_FORMAT_ERROR, f"final states '{', '.join(values)}' have to be in states")


def __transitions_check(json_file: dict):
    values: dict = json_file['transitions']
    transition_keys: list[str] = ['read', 'to_state', 'write', 'action']
    transition_actions: list[str] = ['LEFT', 'RIGHT']

    if __is_not_dict(values):
        Error.throw(Error.FAIL, Error.TYPE_ERROR, "transitions have to be contained in a dict")
    elif __is_not_in(values.keys(), json_file['states']):
        Error.throw(Error.FAIL, Error.JSON_FORMAT_ERROR,
                    f"transitions '{', '.join(values.keys())}' have to be in states")
    for transition_state in values.values():
        if __is_not_list(transition_state):
            Error.throw(Error.FAIL, Error.TYPE_ERROR, "transitions states description have to be contained in a list")
        elif __is_empty([transition_state]):
            Error.throw(Error.FAIL, Error.EMPTY_FIELD_ERROR, "transitions states description can't be empty")
        for transition in transition_state:
            if list(transition.keys()) != transition_keys:
                Error.throw(Error.FAIL, Error.JSON_FORMAT_ERROR,
                            f"transitions descriptions must have '{', '.join(transition_keys)}' fields")
            elif __is_not_in([transition['read']], json_file['alphabet']):
                Error.throw(Error.FAIL, Error.JSON_FORMAT_ERROR,
                            f"transition read character '{transition['read']}' should be part of the alphabet")
            elif __is_not_in([transition['to_state']], json_file['states']):
                Error.throw(Error.FAIL, Error.JSON_FORMAT_ERROR,
                            f"transition to_state '{transition['to_state']}' should be in states")
            elif __is_not_in([transition['write']], json_file['alphabet']):
                Error.throw(Error.FAIL, Error.JSON_FORMAT_ERROR,
                            f"transition write character '{transition['write']}' should be part of the alphabet")
            elif __is_not_in([transition['action']], transition_actions):
                Error.throw(Error.FAIL, Error.JSON_FORMAT_ERROR,
                            f"transition action '{transition['action']}' should be 'LEFT' or 'RIGHT'")
