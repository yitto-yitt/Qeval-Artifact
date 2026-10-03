# EVAL_META: task_id=23, framework=qiskit, class=3
from qiskit import QuantumCircuit

def dj_constant_oracle():
    qc = QuantumCircuit(3)
    # Apply X gate to qubit 2 to make it always output 1 regardless of input
    qc.x(2)
    return qc
