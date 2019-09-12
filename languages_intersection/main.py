import json
from itertools import product


class CFG:
    def __init__(self, nonterminals=None, terminals=None, rules=None, start=None):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.rules = rules
        self.start = start

    def load(self, path):
        with open(path, 'r') as f:
            g = json.load(f)
        self.nonterminals = list(g['nonterminals'])
        self.terminals = list(g['terminals'])
        self.rules = g['rules']
        self.start = g['start']
        return self

    def write(self, path):
        with open(path, 'w') as f:
            json.dump({
                'nonterminals': self.nonterminals,
                'terminals': self.terminals,
                'rules': self.rules,
                'start': self.start
            }, f, indent=4)


class DFA:
    def load(self, path):
        with open(path, 'r') as f:
            g = json.load(f)
        self.states = g['states']
        self.alphabet = g['alphabet']
        self.rules = g['rules']
        self.start = g['start']
        self.accept = g['accept']
        return self


def intersect(cfg: CFG, dfa: DFA):
    new_start = cfg.start
    new_rules = {new_start: []}
    new_nonterminals = set(new_start)
    new_terminals = set()

    for v in dfa.accept:
        right_nonterminal = str(f'[{dfa.start}, {cfg.start}, {v}]')
        new_rules[new_start].append(right_nonterminal)
        new_nonterminals.add(right_nonterminal)

    for left, rights in cfg.rules.items():
        for right in rights:
            for states in product(dfa.states, repeat=len(right) + 1):
                left_nonterminal = f'[{states[0]}, {left}, {states[-1]}]'
                new_rules.setdefault(left_nonterminal, [])
                new_nonterminals.add(left_nonterminal)

                right_part = []
                for i in range(len(right)):
                    right_nonterminal = f'[{states[i]}, {right[i]}, {states[i+1]}]'
                    right_part.append(right_nonterminal)
                    new_nonterminals.add(right_nonterminal)
                new_rules[left_nonterminal].append(right_part)

    for rule in dfa.rules:
        left_nonterminal = f'[{rule[0]}, {rule[1]}, {rule[2]}]'
        new_rules.setdefault(left_nonterminal, [])
        new_rules[left_nonterminal].append([rule[1]])
        new_nonterminals.add(left_nonterminal)
        new_terminals.add(rule[1])

    return CFG(sorted(list(new_nonterminals)), sorted(list(new_terminals)), new_rules, new_start)


cfg = CFG().load('cf_grammar_example.json')
dfa = DFA().load('pda_example.json')

intersect_cfg = intersect(cfg, dfa)
intersect_cfg.write('intersection.json')
