# EVAL_META: task_id=6, framework=qiskit, class=2
from qiskit import QuantumCircuit

def create_state_prep(num_qubits):
    qc = QuantumCircuit(num_qubits)
    qc.x(range(num_qubits))
    return qc
