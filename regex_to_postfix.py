import sys

OPERATORS = {
    '*': (3, 'left'),
    '+': (3, 'left'),
    '?': (3, 'left'),
    '.': (2, 'left'),
    '|': (1, 'left'),
}


def insert_concat(pattern: str) -> str:
    result_chars = []
    for index, current_char in enumerate(pattern):
        # append the current character
        result_chars.append(current_char)
        # check if concatenation operator is needed between current and next character
        if index + 1 < len(pattern):
            next_char = pattern[index + 1]
            if current_char not in ('(', '|') and next_char not in (')', '|', '*', '+', '?'):
                result_chars.append('.')
    return ''.join(result_chars)


def regex_to_postfix(infix_pattern: str) -> str:
    # insert explicit concatenation operators
    augmented_pattern = insert_concat(infix_pattern)
    postfix_chars = []
    operator_stack = []

    for token in augmented_pattern:
        if token == '(':
            operator_stack.append(token)
        elif token == ')':
            # pop operators until matching '(' is found
            while operator_stack and operator_stack[-1] != '(':
                postfix_chars.append(operator_stack.pop())
            operator_stack.pop()  # remove '(' from stack
        elif token in OPERATORS:
            curr_prec, curr_assoc = OPERATORS[token]
            while operator_stack and operator_stack[-1] != '(' and operator_stack[-1] in OPERATORS:
                top_prec, _ = OPERATORS[operator_stack[-1]]
                if top_prec > curr_prec or (top_prec == curr_prec and curr_assoc == 'left'):
                    postfix_chars.append(operator_stack.pop())
                else:
                    break
            operator_stack.append(token)
        else:
            # operand symbol: add directly to postfix output
            postfix_chars.append(token)

    # pop any remaining operators from the stack
    while operator_stack:
        postfix_chars.append(operator_stack.pop())

    return ''.join(postfix_chars)
