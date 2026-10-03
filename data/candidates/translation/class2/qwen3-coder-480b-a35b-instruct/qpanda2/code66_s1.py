# EVAL_META: task_id=66, framework=qpanda2, class=2
import pyqpanda as pq
from math import acos, sqrt


def w_state():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    prog = pq.QProg()
    
    prog.insert(pq.RY(qubits[0], 2 * acos(1 / sqrt(3))))
    prog.insert(pq.CH(qubits[0], qubits[1]))
    prog.insert(pq.CNOT(qubits[1], qubits[2]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.X(qubits[0]))
    
    # Measure all qubits
    for qubit in qubits:
        prog.insert(pq.Measure(qubit, pq.QVec()))
        
    return prog
