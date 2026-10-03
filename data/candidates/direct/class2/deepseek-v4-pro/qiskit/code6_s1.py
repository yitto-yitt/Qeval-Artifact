# EVAL_META: task_id=6, framework=qiskit, class=2
from qiskit import QuantumCircuit

def create_state_prep(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for i in range(num_qubits):
        qc.x(i)
    return qc
