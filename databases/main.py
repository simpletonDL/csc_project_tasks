from collections import Counter

# input = lambda: '+10*2*3 +10*3*2'

a, b = input().split(' ')


def split_expression(s: str):
    res = [[]]
    prev_id = 0
    cur = s[0]
    for i in range(1, len(s)):
        if s[i] in ('+', '*'):
            if s[i] == cur:
                res[-1].append(s[prev_id:i])
                prev_id = i
            else:
                res[-1].append(s[prev_id:i])
                res.append([])
                prev_id = i
                cur = s[i]
    res[-1].append(s[prev_id:])
    return res


def is_expressions_equal(a, b):
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if Counter(x) != Counter(y):
            return False
    return True


a = split_expression(a)
b = split_expression(b)

print(str(is_expressions_equal(a, b)))
