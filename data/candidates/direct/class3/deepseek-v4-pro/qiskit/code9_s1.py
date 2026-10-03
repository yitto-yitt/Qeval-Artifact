# EVAL_META: task_id=9, framework=qiskit, class=3
from qiskit.circuit.library import EfficientSU2

def create_efficientSU2():
    """Return an EfficientSU2 circuit with 3 qubits, 1 repetition, and barriers inserted."""
    return EfficientSU2(3, reps=1, insert_barriers=True)
