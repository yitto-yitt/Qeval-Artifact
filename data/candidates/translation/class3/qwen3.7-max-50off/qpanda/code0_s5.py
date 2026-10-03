# EVAL_META: task_id=0, framework=qpanda, class=3
from pyqpanda3.core import QProg, qalloc

def create_quantum_circuit(n_qubits):
    q = qalloc(n_qubits)
    prog = QProg()
    return q, prog
