# EVAL_META: task_id=36, framework=pennylane, class=3
import pennylane as qml

def bv_function(s):
    n = len(s)
    ops = []
    used_wires = set()

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            ops.append(qml.CNOT(wires=[index, n]))
            used_wires.add(index)
            used_wires.add(n)

    for wire in range(n + 1):
        if wire not in used_wires:
            ops.append(qml.Identity(wires=wire))

    return qml.tape.QuantumScript(ops, [])
