# EVAL_META: task_id=12, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def get_unitary():
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    
    unitary = pq.get_unitary_matrix(prog, qubits)
    return unitary

result = get_unitary()
machine.finalize()
