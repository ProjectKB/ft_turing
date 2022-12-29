import subprocess

OKGREEN = '\033[92m'
ENDC = '\033[0m'

FILE_FORMAT_BASIC = "fileFormatBasic"
FILE_FORMAT_GENERAL = "fileFormatGeneral"
FILE_FORMAT_ALPHABET = "fileFormatAlphabet"
FILE_FORMAT_NAME = "fileFormatName"
FILE_FORMAT_BLANK = "fileFormatBlank"
FILE_FORMAT_STATES = "fileFormatStates"
FILE_FORMAT_INITIAL = "fileFormatInitial"
FILE_FORMAT_FINALS = "fileFormatFinals"
FILE_FORMAT_TRANSITIONS = "fileFormatTransitions"


def launch(path, input='test'):
    return str(subprocess.run(["python3", "main.py", "-f", path, "-i", input], capture_output=True).stdout)


def print_success(type, message, start=''):
    print(f"{start}\n\t{'['+type+']':<{23}} -> {OKGREEN}{message:<{24}}{ENDC} -> ", end=' ')


def test_file_basic_not_found():
    output = launch("machine/invalid/basic_not_found.json")
    assert "file not found" in output
    print_success(FILE_FORMAT_BASIC, 'is not found')


def test_file_basic_is_unicode():
    output = launch("machine/invalid/unicode")
    assert "'utf-8' codec can't decode byte" in output
    print_success(FILE_FORMAT_BASIC, 'is unicode')


def test_file_basic_permission_denied():
    output = launch("machine/invalid/no_right")
    assert "permission denied" in output
    print_success(FILE_FORMAT_BASIC, 'permission denied')


def test_file_basic_json_error():
    output = launch("machine/invalid/json_decode_error.json")
    assert "JSON decode error" in output
    print_success(FILE_FORMAT_BASIC, 'is not valid')


def test_file_general_missing_key():
    output = launch("machine/invalid/general_missing_name_key.json")
    assert "primary keys has to be: name, alphabet, blank, states, initial, finals, transitions" in output
    print_success(FILE_FORMAT_GENERAL, 'missing key name', "\n")


def test_file_general_empty_key():
    output = launch("machine/invalid/general_empty_name_key.json")
    assert "primary values can\'t be empty" in output
    print_success(FILE_FORMAT_GENERAL, 'empty key name')


def test_file_alphabet_type():
    output = launch("machine/invalid/alphabet_type.json")
    assert "alphabet has to be contained in a list" in output
    print_success(FILE_FORMAT_ALPHABET, 'is bad type', "\n")


def test_file_alphabet_is_empty():
    output = launch("machine/invalid/alphabet_empty.json")
    assert "alphabet can't be empty" in output
    print_success(FILE_FORMAT_ALPHABET, 'is empty')


def test_file_alphabet_is_string():
    output = launch("machine/invalid/alphabet_string.json")
    assert "alphabet values have to be string" in output
    print_success(FILE_FORMAT_ALPHABET, 'is not string')


def test_file_alphabet_is_unique():
    output = launch("machine/invalid/alphabet_unique.json")
    assert "alphabet values have to be unique" in output
    print_success(FILE_FORMAT_ALPHABET, 'is not unique')


def test_file_alphabet_is_size_one():
    output = launch("machine/invalid/alphabet_size.json")
    assert "alphabet values have to be size 1" in output
    print_success(FILE_FORMAT_ALPHABET, 'is not size one')


def test_file_name_is_string():
    output = launch("machine/invalid/name_string.json")
    assert "name has to be a string" in output
    print_success(FILE_FORMAT_NAME, 'is not string', "\n")


def test_file_blank_is_string():
    output = launch("machine/invalid/blank_string.json")
    assert "blank character has to be a string" in output
    print_success(FILE_FORMAT_BLANK, 'is not string', "\n")


def test_file_blank_is_alphabet():
    output = launch("machine/invalid/blank_alphabet.json")
    assert "should be part of the alphabet" in output
    print_success(FILE_FORMAT_BLANK, 'is not in alphabet')


def test_file_states_type():
    output = launch("machine/invalid/states_type.json")
    assert "states have to be contained in a list" in output
    print_success(FILE_FORMAT_STATES, 'is bad type', "\n")


def test_file_states_is_empty():
    output = launch("machine/invalid/states_empty.json")
    assert "states can't be empty" in output
    print_success(FILE_FORMAT_STATES, 'is empty')


def test_file_states_is_string():
    output = launch("machine/invalid/states_string.json")
    assert "states values have to be string" in output
    print_success(FILE_FORMAT_STATES, 'is not string')


def test_file_states_is_unique():
    output = launch("machine/invalid/states_unique.json")
    assert "states values have to be unique" in output
    print_success(FILE_FORMAT_STATES, 'is not unique')


def test_file_initial_is_string():
    output = launch("machine/invalid/initial_string.json")
    assert "initial state has to be a string" in output
    print_success(FILE_FORMAT_INITIAL, 'is not string', "\n")


def test_file_initial_is_state():
    output = launch("machine/invalid/initial_state.json")
    assert "should be one of states" in output
    print_success(FILE_FORMAT_INITIAL, 'is not in state')


def test_file_finals_type():
    output = launch("machine/invalid/finals_type.json")
    assert "final states have to be contained in a list" in output
    print_success(FILE_FORMAT_FINALS, 'is bad type', "\n")


def test_file_finals_is_string():
    output = launch("machine/invalid/finals_string.json")
    assert "final states have to be string" in output
    print_success(FILE_FORMAT_FINALS, 'is not string')


def test_file_finals_is_unique():
    output = launch("machine/invalid/finals_unique.json")
    assert "final states have to be unique" in output
    print_success(FILE_FORMAT_FINALS, 'is not unique')


def test_file_finals_is_state():
    output = launch("machine/invalid/finals_state.json")
    assert "have to be in states" in output
    print_success(FILE_FORMAT_FINALS, 'is not in state')


def test_file_transitions_type():
    output = launch("machine/invalid/transitions_type.json")
    assert "transitions have to be contained in a dict" in output
    print_success(FILE_FORMAT_TRANSITIONS, 'is bad type', "\n")


def test_file_transitions_is_state():
    output = launch("machine/invalid/transitions_state.json")
    assert "have to be in states" in output
    print_success(FILE_FORMAT_TRANSITIONS, 'is not in state')


def test_file_transitions_description_type():
    output = launch("machine/invalid/transitions_description_type.json")
    assert "transitions states description have to be contained in a list" in output
    print_success(FILE_FORMAT_TRANSITIONS, 'description is bad type')


def test_file_transitions_description_is_empty():
    output = launch("machine/invalid/transitions_description_empty.json")
    assert "transitions states description can't be empty" in output
    print_success(FILE_FORMAT_TRANSITIONS, 'description is empty')


def test_file_transitions_description_is_valid():
    output = launch("machine/invalid/transitions_description_valid.json")
    assert "transitions descriptions must have" in output
    print_success(FILE_FORMAT_TRANSITIONS, 'description is not valid')


def test_file_transitions_read_is_alphabet():
    output = launch("machine/invalid/transitions_read_alphabet.json")
    assert "should be part of the alphabet" in output
    print_success(FILE_FORMAT_TRANSITIONS, 'read is not in alphabet')


def test_file_transitions_to_state_is_state():
    output = launch("machine/invalid/transitions_to_state_state.json")
    assert "should be in states" in output
    print_success(FILE_FORMAT_TRANSITIONS, 'to_state is not in state')


def test_file_transitions_write_is_alphabet():
    output = launch("machine/invalid/transitions_write_alphabet.json")
    assert "should be part of the alphabet" in output
    print_success(FILE_FORMAT_TRANSITIONS, 'write is not in alphabet')


def test_file_transitions_action_is_valid():
    output = launch("machine/invalid/transitions_action.json")
    assert "should be 'LEFT' or 'RIGHT'" in output
    print_success(FILE_FORMAT_TRANSITIONS, 'action is not valid')
