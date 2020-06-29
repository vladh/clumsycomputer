#!/usr/bin/env python


def is_start(char):
    return char == '^'


def is_end(char):
    return char == '$'


def is_star(char):
    return char == '*'


def is_plus(char):
    return char == '+'


def is_question(char):
    return char == '?'


def is_operator(char):
    return is_star(char) or is_plus(char) or is_question(char)


def is_dot(char):
    return char == '.'


def is_escape_sequence(term):
    return is_escape(term[0])


def is_escape(char):
    return char == '\\'


def is_open_alternate(char):
    return char == '('


def is_close_alternate(char):
    return char == ')'


def is_open_set(char):
    return char == '['


def is_close_set(char):
    return char == ']'


def is_literal(char):
    return char.isalpha() or char.isdigit() or char in ' :/'


def is_alternate(term):
    return is_open_alternate(term[0]) and is_close_alternate(term[-1])


def is_set(term):
    return is_open_set(term[0]) and is_close_set(term[-1])


def is_unit(term):
    return is_literal(term[0]) or is_dot(term[0]) or is_set(term) or is_escape_sequence(term)


def split_alternate(alternate):
    return alternate[1:-1].split('|')


def split_set(set_head):
    set_inside = set_head[1:-1]
    set_terms = list(set_inside)
    return set_terms


def split_expr(expr):
    head = None
    operator = None
    rest = None
    last_expr_pos = 0

    if is_open_set(expr[0]):
        last_expr_pos = expr.find(']') + 1
        head = expr[:last_expr_pos]
    elif is_open_alternate(expr[0]):
        last_expr_pos = expr.find(')') + 1
        head = expr[:last_expr_pos]
    elif is_escape(expr[0]):
        last_expr_pos += 2
        head = expr[:2]
    else:
        last_expr_pos = 1
        head = expr[0]

    if last_expr_pos < len(expr) and is_operator(expr[last_expr_pos]):
        operator = expr[last_expr_pos]
        last_expr_pos += 1

    rest = expr[last_expr_pos:]

    return head, operator, rest


def does_unit_match(expr, string):
    head, operator, rest = split_expr(expr)

    if len(string) == 0:
        return False
    if is_literal(head):
        return expr[0] == string[0]
    elif is_dot(head):
        return True
    elif is_escape_sequence(head):
        if head == '\\a':
            return string[0].isalpha()
        elif head == '\\d':
            return string[0].isdigit()
        else:
            return False
    elif is_set(head):
        set_terms = split_set(head)
        return string[0] in set_terms

    return False


def match_multiple(expr, string, match_length, min_match_length=None, max_match_length=None):
    head, operator, rest = split_expr(expr)

    if not min_match_length:
        min_match_length = 0

    submatch_length = -1

    while not max_match_length or (submatch_length < max_match_length):
        [subexpr_matched, subexpr_length] = match_expr(
            (head * (submatch_length + 1)), string, match_length
        )
        if subexpr_matched:
            submatch_length += 1
        else:
            break

    while submatch_length >= min_match_length:
        [matched, new_match_length] = match_expr(
            (head * submatch_length) + rest, string, match_length
        )
        if matched:
            return [matched, new_match_length]
        submatch_length -= 1

    return [False, None]


def match_star(expr, string, match_length):
    return match_multiple(expr, string, match_length, None, None)


def match_plus(expr, string, match_length):
    return match_multiple(expr, string, match_length, 1, None)


def match_question(expr, string, match_length):
    return match_multiple(expr, string, match_length, 0, 1)


def match_alternate(expr, string, match_length):
    head, operator, rest = split_expr(expr)
    options = split_alternate(head)

    for option in options:
        [matched, new_match_length] = match_expr(
            option + rest, string, match_length
        )
        if matched:
            return [matched, new_match_length]

    return [False, None]


def match_expr(expr, string, match_length=0):
    if len(expr) == 0:
        return [True, match_length]
    elif is_end(expr[0]):
        if len(string) == 0:
            return [True, match_length]
        else:
            return [False, None]

    head, operator, rest = split_expr(expr)

    if is_star(operator):
        return match_star(expr, string, match_length)
    elif is_plus(operator):
        return match_plus(expr, string, match_length)
    elif is_question(operator):
        return match_question(expr, string, match_length)
    elif is_alternate(head):
        return match_alternate(expr, string, match_length)
    elif is_unit(head):
        if does_unit_match(expr, string):
            return match_expr(rest, string[1:], match_length + 1)
    else:
        print(f'Unknown token in expr {expr}.')

    return [False, None]


def match(expr, string):
    match_pos = 0
    matched = False
    if is_start(expr[0]):
        max_match_pos = 0
        expr = expr[1:]
    else:
        max_match_pos = len(string) - 1
    while not matched and match_pos <= max_match_pos:
        [matched, match_length] = match_expr(expr, string[match_pos:])
        if matched:
            return [matched, match_pos, match_length]
        match_pos += 1
    return [False, None, None]


def main():
    expr = '^http://(\\a|\\d)+.(com|net|org)'
    string = 'http://clumsy123computer.com/hey/there'
    [matched, match_pos, match_length] = match(expr, string)
    if matched:
        print(f'match_expr({expr}, {string}) = {string[match_pos:match_pos + match_length]}')
    else:
        print(f'match_expr({expr}, {string}) = False')


if __name__ == '__main__':
    main()
