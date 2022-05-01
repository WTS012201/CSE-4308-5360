import sys
import copy

class bnet:
    def __init__(self, tables) -> None:
        self.tables = tables
        self.prob = 0
    #   calculate probability of a case
    def case(self, b, e, a, j, m):
        prob = 1
        prob *= self.tables["b"] if b else 1 - self.tables["b"]
        prob *= self.tables["e"] if e else 1 - self.tables["e"]
        prob *= self.tables["a"][(b, e)] if a else 1 - self.tables["a"][(b, e)]
        prob *= self.tables["j"][(a)] if j else 1 - self.tables["j"][(a)]
        prob *= self.tables["m"][(a)] if m else 1 - self.tables["m"][(a)]
        return prob
    #   generate tuth table for unspecified events
    def truth_vals(self, n):
        if n < 1:
            return [[]]
        subtable = self.truth_vals(n-1)
        return [ row + [v] for row in subtable for v in [0,1] ]

    def computeProbability(self, b, e, a, j, m):
        self.prob = 0
        unspecified = []
        specified = []
        cases = []
        #   determine what events are unspecified
        if b is None:
            unspecified.append('b')
        else:
            specified.append('b')
        if e is None:
            unspecified.append('e')
        else:
            specified.append('e')
        if a is None:
            unspecified.append('a')
        else:
            specified.append('a')
        if j is None:
            unspecified.append('j')
        else:
            specified.append('j')
        if m is None:
            unspecified.append('m')
        else:
            specified.append('m')

        subcases = self.truth_vals(len(unspecified))
        #   for loop joins specified events with all unspecified events
        for case in subcases:
            new_case = {}
            for event in specified:
                new_case[event] = eval(event)
            for i in range(len(case)):
                new_case[unspecified[i]] = case[i]
            cases.append(new_case)
        #   calculate probability of each case and sum them
        for case in cases:
            new_prob = self.case(case["b"], case["e"], case["a"], case["j"], case["m"])
            self.prob += new_prob
        return self.prob

def main(args):
    if not (1 < len(args) < 8):
        print("Invalid argument amount")
        sys.exit()

    events = [e.lower() for e in args[1:]]
    C1 = {"b": None,"e": None,"a": None,"j": None,"m": None}
    C2 = copy.deepcopy(C1)
    tables = {
        "b": 0.001,
        "e": 0.002,
        "a": {
            (True, True): 0.95,
            (True, False): 0.94,
            (False, True): 0.29,
            (False, False): 0.001,
        },
        "j": {(True): 0.90,(False): 0.05,},
        "m": {(True): 0.70,(False): 0.01,}
    }

    for e in events:
        if e == "given":
            break
        C1[e[0]] = e[1] == "t"
    if "given" in events:
        for e in events[events.index("given") + 1:]:
            C1[e[0]] = e[1] == "t"
            C2[e[0]] = e[1] == "t"

    bn = bnet(tables)
    denom = bn.computeProbability(C2["b"], C2["e"], C2["a"], C2["j"], C2["m"]) if "given" in events else 1
    num = bn.computeProbability(C1["b"], C1["e"], C1["a"], C1["j"], C1["m"])
    print("Probability = {:.7f}".format(num / denom))

if __name__ == "__main__":
    main(sys.argv)