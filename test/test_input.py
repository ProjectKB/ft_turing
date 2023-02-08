import subprocess

OKGREEN = '\033[92m'
OKWHITE = '\033[97m'
ENDC = '\033[0m'

INPUT_UNARY_SUB = "inputUnarySub"
INPUT_UNARY_ADD = "inputUnaryAdd"
INPUT_O2N = "input02n"
INPUT_ON1N = "input0n1n"
INPUT_PAL = "inputPal"
INPUT_UNI = "inputUni"
INPUT_ALL = "inputAll"

UNARY_SUB = "./machine/unary_sub.json"
UNARY_ADD = "./machine/unary_add.json"
O2N = "./machine/02n.json"
ON1N = "./machine/0n_1n.json"
PAL = "./machine/palindrome.json"
UNI = "./machine/pseudo_universal.json"


def launch(path, input):
    return str(subprocess.run(["python3", "main.py", path, input], capture_output=True).stdout)


def print_success(type, message, input, start=''):
    print(f"{start}\n\t{'[' + type + ']':<{15}} -> {OKWHITE}{input:<{40}}{ENDC} -> {OKGREEN}{message:<{66}}{ENDC} -> ",
          end=' ')


def test_all_empty():
    input = ""
    output = launch(UNARY_SUB, input)
    assert "invalid syntax: input can't be empty" in output
    print_success(INPUT_ALL, "can't be empty", input)


def test_all_invalid_char():
    input = "#"
    output = launch(UNARY_SUB, input)
    assert "should be part of alphabet" in output
    print_success(INPUT_ALL, "must be in alphabet", input)


def test_all_blank():
    input = "."
    output = launch(UNARY_SUB, input)
    assert "blank character should can't be part of input" in output
    print_success(INPUT_ALL, "can't contain blank character", input)


def test_sub_missing_char():
    input = "1111="
    output = launch(UNARY_SUB, input)
    assert "each character of the alphabet must be present at least once" in output
    print_success(INPUT_UNARY_SUB, "missing char", input, "\n")


def test_sub_equal():
    input = "1=-1"
    output = launch(UNARY_SUB, input)
    assert "'=' should be the last character" in output
    print_success(INPUT_UNARY_SUB, "'=' should be the last character", input)


def test_sub_multi_sub():
    input = "1-1-1="
    output = launch(UNARY_SUB, input)
    assert "you can perform only one subtraction" in output
    print_success(INPUT_UNARY_SUB, "more than one subtraction", input)


def test_sub_multi_equal():
    input = "1-1=="
    output = launch(UNARY_SUB, input)
    assert "'=' can't be present more than once" in output
    print_success(INPUT_UNARY_SUB, "'=' can't be present more than once", input)


def test_sub_missing_right_op():
    input = "1-="
    output = launch(UNARY_SUB, input)
    assert "operands can't be null" in output
    print_success(INPUT_UNARY_SUB, "operand can't be null", input)


def test_sub_signed():
    input = "11-111="
    output = launch(UNARY_SUB, input)
    assert "left operands can't be smaller than right operand" in output
    print_success(INPUT_UNARY_SUB, "left operands can't be smaller than right operand", input)


def test_add_missing_char():
    input = "1111="
    output = launch(UNARY_ADD, input)
    assert "each character of the alphabet must be present at least once" in output
    print_success(INPUT_UNARY_ADD, "missing char", input, "\n")


def test_add_equal():
    input = "1=+1"
    output = launch(UNARY_ADD, input)
    assert "'=' should be the last character" in output
    print_success(INPUT_UNARY_ADD, "'=' should be the last character", input)


def test_add_multi_sub():
    input = "1+1+1="
    output = launch(UNARY_ADD, input)
    assert "you can perform only one addition" in output
    print_success(INPUT_UNARY_ADD, "more than one addition", input)


def test_add_multi_equal():
    input = "1+1=="
    output = launch(UNARY_ADD, input)
    assert "'=' can't be present more than once" in output
    print_success(INPUT_UNARY_ADD, "'=' can't be present more than once", input)


def test_add_missing_right_op():
    input = "1+="
    output = launch(UNARY_ADD, input)
    assert "operands can't be null" in output
    print_success(INPUT_UNARY_ADD, "operand can't be null", input)


def test_02n_y():
    input = "0y"
    output = launch(O2N, input)
    assert "can't contain 'y' or 'n'" in output
    print_success(INPUT_O2N, "contains y", input, "\n")


def test_02n_n():
    input = "0n"
    output = launch(O2N, input)
    assert "can't contain 'y' or 'n'" in output
    print_success(INPUT_O2N, "contains n", input)


def test_0n1n_y():
    input = "01y"
    output = launch(ON1N, input)
    assert "can't contain 'y' or 'n'" in output
    print_success(INPUT_ON1N, "contains y", input, "\n")


def test_0n1n_n():
    input = "01n"
    output = launch(ON1N, input)
    assert "can't contain 'y' or 'n'" in output
    print_success(INPUT_ON1N, "contains n", input)


def test_uni_input():
    input = "{(r1:r1>)(r+:r1>)(r=:eB<)(e1:HH>)|r}1+1="
    output = launch(UNI, input)
    assert "he program part has to be encoded has following" in output
    print_success(INPUT_UNI, "bad program input, should be: {(r1:r1>)(r+:r1>)(r=:eB<)(e1:HB>)|r}", input)

