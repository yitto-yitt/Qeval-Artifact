# EVAL_META: task_id=5, framework=qiskit, class=2

from qiskit import QuantumCircuit

def create_state_prep():
    """
    Returns a 2-qubit QuantumCircuit that prepares the bitstring state "01".
    In Qiskit's little-endian convention, the state "01" corresponds to 
    qubit 0 being in state |1> and qubit 1 being in state |0>.
    """
    qc = QuantumCircuit(2)
    qc.x(0)
    return qc
