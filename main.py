from regex_to_postfix import regex_to_postfix
from postfix_to_nfa import postfix_to_nfa
from nfa_to_dfa import nfa_to_dfa, visualize_dfa, visualize_nfa, print_dfa
from dfa_simulator import simulate_dfa
from test_runner import run_tests

print("Modes: \n1. Regex to DFA \n2. Run test cases")
mode = int(input("Enter the mode: "))

if mode == 1:
    regex = input("Enter the regex: ")
    postfix = regex_to_postfix(regex)
    nfa = postfix_to_nfa(postfix)
    try:
        visualize_nfa(nfa)
    except Exception as e:
        print(e)
    dfa = nfa_to_dfa(nfa)
    print_dfa(dfa)
    try:
        visualize_dfa(dfa)
    except Exception as e:
        print(e)

    print("--------------------------------")
    test_string = input("Enter the string to test: ")
    is_accepted = simulate_dfa(dfa, test_string)
    if is_accepted:
        print("String accepted!")
    else:
        print("String rejected!")
elif mode == 2:
    test_file = input("Enter the test cases JSON file path (e.g. tests.json): ")
    run_tests(test_file)