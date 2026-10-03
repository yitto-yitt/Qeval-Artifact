# EVAL_META: task_id=36, framework=pennylane, class=3
import pennylane as qml

def bv_function(s):
    n = len(s)
    ops = []
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            ops.append(qml.CNOT(wires=[index, n]))
    return ops
