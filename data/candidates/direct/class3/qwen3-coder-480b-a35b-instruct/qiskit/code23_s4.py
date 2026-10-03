# EVAL_META: task_id=23, framework=qiskit, class=3
from qiskit import QuantumCircuit

def dj_constant_oracle():
    qc = QuantumCircuit(3)
    # For a constant-one oracle, we need to flip the output qubit (qubit 2) to |1>
    # regardless of the input values on qubits 0 and 1
    qc.x(2)
    return qc
