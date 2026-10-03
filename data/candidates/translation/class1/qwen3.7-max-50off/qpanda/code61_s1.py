# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg

def create_quantum_circuit_with_one_qubit_and_measure():
    qm = QMachine(1, 1)
    q = qm.qalloc(1)
    c = qm.calloc(1)
    prog = QProg()
    prog.measure(q[0], c[0])
    return prog
