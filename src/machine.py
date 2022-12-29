class Machine:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

    def __init__(self, json_file, input):
        self.tape = list(input)
        self.name = json_file['name']
        self.alphabet = json_file['alphabet']
        self.blank = json_file['blank']
        self.states = json_file['states']
        self.initial = json_file['initial']
        self.finals = json_file['finals']
        self.transitions = json_file['transitions']
        self.state = self.initial
        self.transitions_dict = self.set_transitions_dict()

    def __str__(self):
        description = ""
        description += f"Name: {self.name}\n"
        description += f"Alphabet: [{', '.join(self.alphabet)}]\n"
        description += f"States: [{', '.join(self.states)}]\n"
        description += f"Initial: {self.initial}\n"
        description += f"Finals: [{', '.join(self.finals)}]\n"

        for key, value in self.transitions.items():
            for state in value:
                description += f"({key}, {state['read']}) -> ({state['to_state']}, {state['write']}, {state['action']})\n"

        return description

    def set_transitions_dict(self):
        transitions_dict = {state: {} for state in self.states}

        for key, value in self.transitions.items():
            for state in value:
                transitions_dict[key][state['read']] = {
                    'to_state': state['to_state'],
                    'write': state['write'],
                    'action': state['action']
                }

        return transitions_dict

    def show_tape(self, i):
        print(
            f"[{''.join(self.tape[:i])}{self.OKGREEN}{''.join(self.tape[i])}{self.ENDC}{''.join(self.tape[i + 1:])}{self.blank * 10}] "
            f"({self.state}, {self.tape[i]}) -> "
            f"({self.transitions_dict[self.state][self.tape[i]]['to_state']}, "
            f"{self.transitions_dict[self.state][self.tape[i]]['write']}, "
            f"{self.transitions_dict[self.state][self.tape[i]]['action']})"
        )

    def process(self):
        i = 0
        ended = False
        blocked = False

        while not ended and not blocked:
            self.show_tape(i)
            current = {'state': self.state, 'tape': self.tape[i]}
            self.state = self.transitions_dict[self.state][self.tape[i]]['to_state']
            self.tape[i] = self.transitions_dict[current['state']][self.tape[i]]['write']

            i += 1 if self.transitions_dict[current['state']][current['tape']]['action'] == "RIGHT" else -1

            if self.state in self.finals:
                ended = True

        print(f"[{''.join(self.tape)+'.'*10}]")