# EVAL_META: task_id=12, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def get_unitary():
    circ = pq.QCircuit()
    circ.insert(pq.H(qubits[0]))
    circ.insert(pq.CNOT(qubits[0], qubits[1]))
    prog = pq.QProg()
    prog.insert(circ)
    return pq.get_matrix(prog)

machine.finalize()
