# EVAL_META: task_id=36, framework=pennylane, class=3
import pennylane as qml

def bv_function(s):
    n = len(s)
    def oracle(wires=None):
        if wires is None:
            wires = list(range(n + 1))
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[wires[index], wires[n]])
    return oracle
