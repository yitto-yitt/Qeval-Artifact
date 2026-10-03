# EVAL_META: task_id=26, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, QNode, QGate, Measure, H, CNOT
from pyqpanda3.core import create_qprog, qAlloc, cAlloc


def bell_dag():
    qvm = pq.QVM()
    qvm.init_qvm()
    
    q = [qvm.qAlloc_one() for _ in range(3)]
    c = [qvm.cAlloc_one() for _ in range(3)]
    
    prog = pq.QProg()
    prog.insert(H(q[0]))
    prog.insert(CNOT(q[0], q[1]))
    prog.insert(pq.Measure(q[0], c[0]))
    
    # In pyQPanda3, we don't have a direct DAG representation like Qiskit
    # Instead, we can return the program which represents the circuit structure
    # Since the task asks for a DAG-like structure, we'll return the program
    # which contains the quantum operations in their logical form
    
    return prog
