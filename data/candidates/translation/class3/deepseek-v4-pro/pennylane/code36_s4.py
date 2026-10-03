# EVAL_META: task_id=36, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def bv_function(s):
    n = len(s)
    with QuantumTape() as tape:
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])
    return tape
