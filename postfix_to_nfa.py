from typing import Optional, List, Dict

tokens = ('*', '+', '?', '.', '|')

class State:
    _id_counter = 0

    def __init__(self):
        self.id = State._id_counter
        State._id_counter += 1
        # transitions: symbol -> list of next states; None for epsilon transitions
        self.transitions: Dict[Optional[str], List['State']] = {}

    def add_transition(self, symbol: Optional[str], state: 'State') -> None:
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

class NFAFragment:
    def __init__(self, start: State, accept: State):
        self.start = start
        self.accept = accept


def postfix_to_nfa(postfix: str) -> NFAFragment:
    stack: List[NFAFragment] = []

    for token in postfix:
        if token not in tokens:
            # letter: create fragment start->accept with the symbol
            start = State()
            accept = State()
            start.add_transition(token, accept)
            stack.append(NFAFragment(start, accept))
        elif token == '.':
            # concatenation: pop two fragments and link them
            frag2 = stack.pop()
            frag1 = stack.pop()
            frag1.accept.add_transition(None, frag2.start)
            stack.append(NFAFragment(frag1.start, frag2.accept))
        elif token == '|':
            # pop two fragments and build new branches
            frag2 = stack.pop()
            frag1 = stack.pop()
            start = State()
            accept = State()
            start.add_transition(None, frag1.start)
            start.add_transition(None, frag2.start)
            frag1.accept.add_transition(None, accept)
            frag2.accept.add_transition(None, accept)
            stack.append(NFAFragment(start, accept))
        elif token == '*':
            # zero or more repetitions
            frag = stack.pop()
            start = State()
            accept = State()
            start.add_transition(None, frag.start)
            start.add_transition(None, accept)
            frag.accept.add_transition(None, frag.start)
            frag.accept.add_transition(None, accept)
            stack.append(NFAFragment(start, accept))
        elif token == '+':
            # one or more repetitions
            frag = stack.pop()
            start = State()
            accept = State()
            start.add_transition(None, frag.start)
            frag.accept.add_transition(None, frag.start)
            frag.accept.add_transition(None, accept)
            stack.append(NFAFragment(start, accept))
        elif token == '?':
            # zero or one
            frag = stack.pop()
            start = State()
            accept = State()
            start.add_transition(None, frag.start)
            start.add_transition(None, accept)
            frag.accept.add_transition(None, accept)
            stack.append(NFAFragment(start, accept))
        else:
            raise ValueError(f"Unknown operator: {token}")

    return stack.pop()

