# EVAL_META: task_id=27, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
from pyqpanda3.extensions import *

def apply_op_back():
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    
    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    
    # Convert to DAG representation
    dag_circ = pq.to_DAG(prog)
    
    # Apply Hadamard operation to the back of qubit 0
    h_gate = pq.H(q[0])
    dag_circ.apply_operation_back(h_gate)
    
    qvm.finalize()
    return dag_circ
