import argparse as a

from src.file_parser import file_parser
from src.input_parser import input_parser
from src.machine import get_transitions, get_tape, show, process

if __name__ == '__main__':
    argparse = a.ArgumentParser()

    argparse.add_argument("file", default=False,
                          help="file containing the machine")
    argparse.add_argument("input", default=False,
                          help="input the machine has to process")

    args = argparse.parse_args()

    machine = file_parser(args.file)
    input_parser(args.input, args.file, machine)
    tape = get_tape(args.input, machine)
    transitions = get_transitions(machine)

    show(machine)
    process(machine, tape, transitions)


