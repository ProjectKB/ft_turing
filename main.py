import argparse as a

from src.parser import parse
from src.machine import get_transitions, get_tape, show, process

unary_sub_input_for_pseudo_universal = "{(r1:r1>)(r+:r1>)(r=:e.<)(e1:H.>)|r}11+111="

if __name__ == '__main__':
    argparse = a.ArgumentParser()

    argparse.add_argument("-f", "--file", default=False,
                          help="file containing the machine")
    argparse.add_argument("-i", "--input", default=False,
                          help="input the machine has to process")

    args = argparse.parse_args()

    if not args.file or not args.input:
        argparse.error(
            'you have to provide a file and an input [-i] and [-f].')

    machine = parse(args.file)
    tape = get_tape(args.input, machine)
    transitions = get_transitions(machine)

    show(machine)
    process(machine, tape, transitions)


