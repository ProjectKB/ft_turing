from src.error import Error

UNARY_SUB = "unary_sub.json"
UNARY_ADD = "unary_add.json"
ON1N = "0n_1n.json"
O2N = "02n.json"
UNI = "pseudo_universal.json"
PAL = "palindrome.json"
MACHINES = [UNARY_SUB, UNARY_ADD, O2N, ON1N, UNI, PAL]


def input_parser(input: str, file_name: str, machine: dict):
    name = file_name[file_name.rindex('/') + 1:]

    if input == "":
        Error.throw(Error.FAIL, Error.INPUT_ERROR, "invalid syntax: input can't be empty")
    if invalid_chars := __invalid_char(machine, input):
        Error.throw(Error.FAIL, Error.INPUT_ERROR,
                    f"invalid syntax: {' '.join(invalid_chars)} should be part of alphabet")
    elif __blank_in_input(machine, input):
        Error.throw(Error.FAIL, Error.INPUT_ERROR, "invalid syntax: blank character should can't be part of input")
    elif name == UNARY_SUB:
        __handle_sub(machine, input)
    elif name == UNARY_ADD:
        __handle_add(machine, input)
    elif name == O2N:
        __handle_O2N(machine, input)
    elif name == ON1N:
        __handle_ON1N(machine, input)
    elif name == PAL:
        __handle_pal(machine)
    elif name == UNI:
        __handle_uni(machine, input)


def __handle_uni(machine, input):
    program = "{(r1:r1>)(r+:r1>)(r=:eB<)(e1:HB>)|r}"
    alphabet = ["1", ".", "+", "=", "h", "{", "}", "|", ":", ">", "<", "(", ")", "r", "e", "B", "H"]
    if machine['alphabet'] != alphabet:
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                    f"invalid syntax: alphabet [{' '.join(machine['alphabet'])}] should be [{' '.join(alphabet)}]")
    elif program not in input:
        Error.throw(Error.FAIL, Error.INPUT_ERROR, f"invalid syntax: the program part has to be encoded has following {program}")

    program_input = input.replace(program, '')
    __handle_add({'alphabet': ['1', '.', '+', '='], 'blank': '.'}, program_input)


def __handle_pal(machine):
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z", "."]
    if machine['alphabet'] != alphabet:
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                    f"invalid syntax: alphabet [{' '.join(machine['alphabet'])}] should be [{' '.join(alphabet)}]")


def __handle_ON1N(machine, input):
    alphabet = ['1', '0', '.', 'y', 'n']
    if machine['alphabet'] != alphabet:
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                    f"invalid syntax: alphabet [{' '.join(machine['alphabet'])}] should be [{' '.join(alphabet)}]")
    elif __contain_y_or_n(input):
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, f"invalid syntax: '{input}' can't contain 'y' or 'n'")


def __handle_O2N(machine, input):
    alphabet = ['0', '.', 'y', 'n']
    if machine['alphabet'] != alphabet:
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                    f"invalid syntax: alphabet [{' '.join(machine['alphabet'])}] should be [{' '.join(alphabet)}]")
    elif __contain_y_or_n(input):
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, f"invalid syntax: '{input}' can't contain 'y' or 'n'")


def __handle_add(machine, input):
    if not __alphabet_not_found(machine, input):
        Error.throw(Error.FAIL, Error.INPUT_ERROR, "each character of the alphabet must be present at least once")

    alphabet = ['1', '.', '+', '=']
    if machine['alphabet'] != alphabet:
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                    f"invalid syntax: alphabet [{' '.join(machine['alphabet'])}] should be [{' '.join(alphabet)}]")
    elif input[-1] != '=':
        Error.throw(Error.FAIL, Error.INPUT_ERROR, f"invalid input: in {input} '=' should be the last character")
    elif input.count('+') > 1:
        Error.throw(Error.FAIL, Error.INPUT_ERROR, f"invalid input: you can perform only one addition")
    elif input.count('=') > 1:
        Error.throw(Error.FAIL, Error.INPUT_ERROR, f"invalid input: '=' can't be present more than once")

    left, right = input.split('+')
    if not len(left) or not len(right) or input[-2] == '+':
        Error.throw(Error.FAIL, Error.INPUT_ERROR, f"invalid input: operands can't be null")


def __handle_sub(machine, input):
    if not __alphabet_not_found(machine, input):
        Error.throw(Error.FAIL, Error.INPUT_ERROR, "each character of the alphabet must be present at least once")

    alphabet = ['1', '.', '-', '=']
    if machine['alphabet'] != alphabet:
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                    f"invalid syntax: alphabet [{' '.join(machine['alphabet'])}] should be [{' '.join(alphabet)}]")
    elif input[-1] != '=':
        Error.throw(Error.FAIL, Error.INPUT_ERROR, f"invalid input: in {input} '=' should be the last character")
    elif input.count('-') > 1:
        Error.throw(Error.FAIL, Error.INPUT_ERROR, f"invalid input: you can perform only one subtraction")
    elif input.count('=') > 1:
        Error.throw(Error.FAIL, Error.INPUT_ERROR, f"invalid input: '=' can't be present more than once")

    left, right = input.split('-')
    if not len(left) or not len(right) or input[-2] == '-':
        Error.throw(Error.FAIL, Error.INPUT_ERROR, f"invalid input: operands can't be null")
    elif not len(left) or not len(right) or len(left) < len(right) - 1:
        Error.throw(Error.FAIL, Error.INPUT_ERROR, f"invalid input: left operands can't be smaller than right operand")


def __invalid_char(machine, input):
    return [letter for letter in input if letter not in machine['alphabet']]


def __blank_in_input(machine, input):
    return [letter for letter in input if letter == machine['blank']]


def __alphabet_not_found(machine, input):
    alphabet_checker = {letter: 0 for letter in machine['alphabet'] if letter != machine['blank']}
    for letter in input:
        alphabet_checker[letter] += 1

    try:
        list(alphabet_checker.values()).index(0)
    except:
        return True
    return False


def __contain_y_or_n(input):
    return "y" in input or "n" in input
