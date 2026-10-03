# EVAL_META: task_id=36, framework=pennylane, class=3
import pennylane as qml


def bv_function(s):
    n = len(s)
    with qml.tape.QuantumTape() as oracle:
        for wire in range(n + 1):
            qml.Identity(wires=wire)
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])
    return oracle
