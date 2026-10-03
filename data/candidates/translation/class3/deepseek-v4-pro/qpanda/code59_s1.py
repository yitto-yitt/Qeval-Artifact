# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QProg, allocate_qubits, H, CNOT

def create_cz_gate():
    qubits = allocate_qubits(2)
    prog = QProg()
    prog.insert(H(qubits[1]))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(H(qubits[1]))
    return prog
