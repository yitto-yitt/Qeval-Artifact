# EVAL_META: task_id=23, framework=qiskit, class=3
from qiskit import QuantumCircuit

def dj_constant_oracle():
    # Create a QuantumCircuit with 3 qubits (0 and 1 are inputs, 2 is the output)
    oracle_qc = QuantumCircuit(3)
    # For a constant-one oracle, the output qubit (qubit 2) is always flipped
    oracle_qc.x(2)
    return oracle_qc
