from typing import Set, Dict, FrozenSet
from postfix_to_nfa import NFAFragment, State
import networkx as nx
import matplotlib.pyplot as plt

class DFA:
    def __init__(self, start_state: int, transitions: Dict[int, Dict[str, int]], accept_states: Set[int]):
        self.start_state = start_state
        self.transitions = transitions
        self.accept_states = accept_states


# all states reachable from the given states by epsilon transitions
def epsilon_closure(states: Set[State]) -> Set[State]:
    closure: Set[State] = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for next_state in state.transitions.get(None, []):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

# all states reachable from the given states by the given symbol
def move(nfa_states: Set[State], symbol: str) -> Set[State]:
    result: Set[State] = set()
    for state in nfa_states:
        for next_state in state.transitions.get(symbol, []):
            result.add(next_state)
    return result


def nfa_to_dfa(nfa: NFAFragment) -> DFA:
    # gather input symbols (exclude epsilon)
    symbols: Set[str] = set()
    visited: Set[int] = set()
    stack = [nfa.start]
    while stack:
        state = stack.pop()
        if state.id in visited:
            continue
        visited.add(state.id)
        for sym, targets in state.transitions.items():
            for target in targets:
                stack.append(target)
            if sym is not None:
                symbols.add(sym)

    # mapping from frozenset of NFA states to DFA state id
    dfa_state_map: Dict[FrozenSet[State], int] = {}
    dfa_transitions: Dict[int, Dict[str, int]] = {}
    accept_states: Set[int] = set()

    # initialize start state
    start_set = epsilon_closure({nfa.start})
    dfa_state_map[frozenset(start_set)] = 0
    if nfa.accept in start_set:
        accept_states.add(0)
    unmarked: Set[FrozenSet[State]] = {frozenset(start_set)}

    # process unmarked DFA states
    while unmarked:
        current_fs = unmarked.pop()
        current_id = dfa_state_map[current_fs]
        # convert frozenset back to set of State
        current_set = set(current_fs)
        dfa_transitions[current_id] = {}
        for sym in symbols:
            # compute move then closure
            target_nfa = epsilon_closure(move(current_set, sym))
            if not target_nfa:
                continue
            target_fs = frozenset(target_nfa)
            if target_fs not in dfa_state_map:
                new_id = len(dfa_state_map)
                dfa_state_map[target_fs] = new_id
                if nfa.accept in target_nfa:
                    accept_states.add(new_id)
                unmarked.add(target_fs)
            dfa_transitions[current_id][sym] = dfa_state_map[target_fs]

    return DFA(start_state=0, transitions=dfa_transitions, accept_states=accept_states) 

def visualize_nfa(nfa: NFAFragment) -> None:
    G = nx.MultiDiGraph()
    visited = set()
    def add_edges(state: State):
        if state.id in visited:
            return
        visited.add(state.id)
        G.add_node(state.id)
        for symbol, targets in state.transitions.items():
            for target in targets:
                label = 'ε' if symbol is None else symbol
                G.add_edge(state.id, target.id, label=label)
                add_edges(target)
    add_edges(nfa.start)
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    edge_labels = nx.get_edge_attributes(G, 'label')
    plt.figure(figsize=(8,6))
    # highlight start and accept states
    color_map = []
    for node in G.nodes():
        if node == nfa.start.id:
            color_map.append('green')
        elif node == nfa.accept.id:
            color_map.append('red')
        else:
            color_map.append('lightblue')
    nx.draw(G, pos, with_labels=True, node_color=color_map, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

def visualize_dfa(dfa: DFA) -> None:
    G = nx.MultiDiGraph()
    visited = set()
    def add_edges(state: int):
        if state in visited:
            return
        visited.add(state)
        G.add_node(state)
        for sym, dst in dfa.transitions[state].items():
            G.add_edge(state, dst, label=sym)
            add_edges(dst)
    add_edges(dfa.start_state)
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    edge_labels = nx.get_edge_attributes(G, 'label')
    plt.figure(figsize=(8,6))
    # highlight start and accept states
    color_map = []
    for node in G.nodes():
        if node == dfa.start_state:
            color_map.append('green')
        elif node in dfa.accept_states:
            color_map.append('red')
        else:
            color_map.append('lightblue')
    nx.draw(G, pos, with_labels=True, node_color=color_map, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()
    
def print_dfa(dfa: DFA) -> None:
    print("Start state:", dfa.start_state)
    print("Accept states:", *sorted(dfa.accept_states))
    print("Transitions:")
    for state in sorted(dfa.transitions):
        for symbol, to_state in sorted(dfa.transitions[state].items()):
            print(f"  {state} -- {symbol} --> {to_state}")
