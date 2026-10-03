# EVAL_META: task_id=9, framework=qiskit, class=3

from qiskit.circuit.library import EfficientSU2

def create_efficientSU2():
    """
    Generate an EfficientSU2 circuit with 3 qubits, 1 reps and insert_barriers=True.
    """
    return EfficientSU2(num_qubits=3, reps=1, insert_barriers=True)
