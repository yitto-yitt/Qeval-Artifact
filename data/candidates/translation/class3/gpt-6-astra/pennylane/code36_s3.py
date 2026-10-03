# EVAL_META: task_id=36, framework=pennylane, class=3
import pennylane as qml

def bv_function(s):
    n = len(s)
    operations = [
        qml.CNOT(wires=[index, n])
        for index, bit in enumerate(reversed(s))
        if bit == "1"
    ]
    return qml.tape.QuantumScript(operations)
