# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def synthesize_evolution_gate(pauli_string, time):
    wires = list(range(len(pauli_string)))
    with QuantumTape() as tape:
        qml.PauliRot(2 * time, pauli_string, wires=wires)
    return tape
