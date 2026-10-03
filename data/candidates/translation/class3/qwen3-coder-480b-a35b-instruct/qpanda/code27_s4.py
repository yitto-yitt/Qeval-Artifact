# EVAL_META: task_id=27, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, QNode, QGate, H, CNOT
from pyqpanda3.core import create_qprog, qAlloc, cAlloc


def apply_op_back():
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    
    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    
    # In pyqpanda3, we work directly with programs rather than DAGs
    # We'll simulate the DAG behavior by creating a new program with the additional operation
    new_prog = prog
    new_prog.insert(pq.H(q[0]))  # Apply H gate to qubit 0 at the end
    
    return new_prog
