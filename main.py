import argparse as a

from src.parser import parse

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

    parse(args.file)
