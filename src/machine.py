def show(machine: dict):
    print(
        f"Name: {machine['name']}\n"
        f"Alphabet: [{', '.join(machine['alphabet'])}]\n"
        f"States: [{', '.join(machine['states'])}]\n"
        f"Initial: {machine['initial']}\n"
        f"Finals: [{', '.join(machine['finals'])}]"
    )

    for key, value in machine['transitions'].items():
        for state in value:
            print(f"({key}, {state['read']}) -> ({state['to_state']}, {state['write']}, {state['action']})")


def get_transitions(machine: dict) -> dict:
    transitions: dict = {state: {} for state in machine['states']}

    for key, value in machine['transitions'].items():
        for state in value:
            transitions[key][state['read']] = {
                'to_state': state['to_state'],
                'write': state['write'],
                'action': state['action']
            }

    return transitions


def get_tape(input: str, machine: dict) -> list[str]:
    return list(input) + list(machine['blank'] * 10)


def process(machine: dict, tape: list[str], transitions: dict):
    head: int = 0
    ended: bool = False
    blocked: bool = False
    state: str = machine['initial']

    while not ended and not blocked:
        __show_tape(tape, transitions, state, head)

        current: dict = __get_current(state, tape, head)
        tape[head] = __get_head(transitions, current)
        state = __get_state(transitions, current)
        head += __move_head(transitions, current)

        if state in machine['finals']:
            ended = True

    print(f"[{''.join(tape)}]")


def __show_tape(tape: list[str], transitions: dict, state: str, head: int):
    print(
        f"[{''.join(tape[:head])}\033[92m{''.join(tape[head])}\033[0m{''.join(tape[head + 1:])}] "
        f"({state}, {tape[head]}) -> "
        f"({transitions[state][tape[head]]['to_state']}, "
        f"{transitions[state][tape[head]]['write']}, "
        f"{transitions[state][tape[head]]['action']})"
    )


def __get_current(state: str, tape: str, head: int) -> dict:
    return {'state': state, 'head': tape[head]}


def __get_head(transitions: dict, current: dict) -> str:
    return transitions[current['state']][current['head']]['write']


def __get_state(transitions: dict, current: dict) -> str:
    return transitions[current['state']][current['head']]['to_state']


def __move_head(transitions: dict, current: dict) -> int:
    return 1 if transitions[current['state']][current['head']]['action'] == "RIGHT" else -1
