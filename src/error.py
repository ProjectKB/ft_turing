import sys


class Error:
    # Colors
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Error Names
    FILE_NOT_FOUND_ERROR = "FileNotFoundError"
    IS_A_DIRECTORY_ERROR = "IsADirectoryError"
    PERMISSION_ERROR = "PermissionError"
    UNICODE_DECODE_ERROR = "UnicodeDecodeError"
    FILE_FORMAT_ERROR = "FileFormatError"
    KEYBOARD_INTERRUPT_ERROR = "KeyboardInterruptError"
    JSON_DECODE_ERROR = "JSONDecodeError"
    JSON_FORMAT_ERROR = "JSONFormatError"
    EMPTY_FIELD_ERROR = "EmptyFieldError"
    UNHANDLED_FILE_ERROR = "UnhandledFileError"
    TYPE_ERROR = "TypeError"
    REPETITION_ERROR = "RepetitionError"
    SIZE_ERROR = "SizeError"
    INPUT_ERROR = "InputError"

    @staticmethod
    def print_error(*msg):
        for m in msg:
            print(m)
        sys.exit(0)

    @staticmethod
    def throw(level, type, msg):
        print(f"\n\t{level}[{type}] -> {Error.ENDC}{msg}\n")
        sys.exit(0)
