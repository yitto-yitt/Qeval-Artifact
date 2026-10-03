# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import QuantumCircuit


def create_state_prep(num_qubits):
    qc = QuantumCircuit(num_qubits)
    qc.x(0)
    return qc
