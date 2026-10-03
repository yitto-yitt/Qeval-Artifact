# EVAL_META: task_id=12, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np


def get_unitary():
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    
    unitary = pq.get_unitary_matrix(prog, qubits)
    machine.qFree_all(qubits)
    return unitary
