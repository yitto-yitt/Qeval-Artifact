# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QProg, allocateQubits, SX

def create_c3sx_circuit():
    prog = QProg()
    qubits = allocateQubits(4)
    c3sx = SX(qubits[3]).controlled_by([qubits[0], qubits[1], qubits[2]])
    prog << c3sx
    return prog
