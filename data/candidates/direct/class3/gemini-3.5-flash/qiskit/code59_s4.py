# EVAL_META: task_id=59, framework=qiskit, class=3

from qiskit import QuantumCircuit

def create_cz_gate():
    """Design a CZ gate using only H and CNOT gates and return the quantum circuit."""
    qc = QuantumCircuit(2)
    qc.h(1)
    qc.cx(0, 1)
    qc.h(1)
    return qc
