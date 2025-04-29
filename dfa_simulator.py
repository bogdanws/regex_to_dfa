from nfa_to_dfa import DFA


def simulate_dfa(dfa_obj: DFA, input_string: str) -> bool:
    current_state = dfa_obj.start_state

    # process each symbol in the input
    for symbol in input_string:
        state_transitions = dfa_obj.transitions.get(current_state, {})
        if symbol not in state_transitions:
            return False
        # move to the next state
        current_state = state_transitions[symbol]

    return current_state in dfa_obj.accept_states 