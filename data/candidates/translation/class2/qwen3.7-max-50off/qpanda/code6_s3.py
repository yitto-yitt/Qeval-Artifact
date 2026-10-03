# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit

def create_state_prep(num_qubits):
    qc = QuantumCircuit(num_qubits)
    qc.x(0)
    return qc
