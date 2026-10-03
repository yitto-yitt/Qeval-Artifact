# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def synthesize_evolution_gate(pauli_string, time):
    """Synthesize the evolution gate for a Pauli string and time."""
    n = len(pauli_string)
    op = qml.PauliRot(2 * time, pauli_string, wires=range(n))
    return QuantumScript([op])
