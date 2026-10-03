# EVAL_META: task_id=23, framework=qiskit, class=3

from qiskit import QuantumCircuit

def dj_constant_oracle():
    """
    Creates a constant-one oracle for a Deutsch-Jozsa experiment.
    The oracle takes 2 input qubits (0 and 1) and 1 output qubit (2).
    For a constant-one oracle, the output qubit is always flipped (X gate on qubit 2).
    """
    oracle_qc = QuantumCircuit(3)
    oracle_qc.x(2)
    return oracle_qc
