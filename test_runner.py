import json
import sys
from regex_to_postfix import regex_to_postfix
from postfix_to_nfa import postfix_to_nfa
from nfa_to_dfa import nfa_to_dfa
from dfa_simulator import simulate_dfa


def run_tests(test_file: str) -> None:
    try:
        with open(test_file, 'r') as file:
            test_definitions = json.load(file)
    except IOError:
        print(f"Error: could not open test file {test_file}")
        sys.exit(1)

    total_tests = 0
    passed_tests = 0

    for case in test_definitions:
        name = case.get('name', '')
        regex = case['regex']
        postfix = regex_to_postfix(regex)
        nfa = postfix_to_nfa(postfix)
        dfa = nfa_to_dfa(nfa)

        for test in case.get('test_strings', []):
            input_str = test.get('input', '')
            expected = test.get('expected', False)
            total_tests += 1

            result = simulate_dfa(dfa, input_str)
            if result == expected:
                status = 'PASS'
                passed_tests += 1
            else:
                status = 'FAIL'

            print(f"{name}: regex='{regex}' input='{input_str}' expected={expected} result={result} => {status}")

    print(f"\n{passed_tests}/{total_tests} tests passed.") 