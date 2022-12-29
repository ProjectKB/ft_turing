import subprocess

OKGREEN = '\033[92m'
ENDC = '\033[0m'

PALINDROME = 'palindrome'
FILE = "machine/palindrome.json"

def launch(input):
    return subprocess.run(["python3", "main.py", "-f", FILE, "-i", input], capture_output=True).stdout


def print_success(type, message, start=''):
    print(f"{start}\n\t{'['+type+']':<{23}} -> {OKGREEN}{message:<{24}}{ENDC} -> ", end=' ')


def test_palindrome_basic():
    output = launch("machine/palindrome.json")
    print(output)
