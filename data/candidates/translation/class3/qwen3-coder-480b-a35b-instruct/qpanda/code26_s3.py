# EVAL_META: task_id=26, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, QNode, QGate, Measure, H, CNOT, QVec
from pyqpanda3.core import create_qprog, qAlloc, cAlloc


def bell_dag():
    machine = pq.QMachine()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.Measure(q[0], c[0]))
    
    # In pyQPanda3, we don't have a direct DAG representation like Qiskit
    # We return the quantum program which represents the circuit structure
    return prog
