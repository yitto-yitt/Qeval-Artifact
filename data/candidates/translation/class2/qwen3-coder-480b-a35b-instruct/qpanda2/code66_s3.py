# EVAL_META: task_id=66, framework=qpanda2, class=2
import pyqpanda as pq
from numpy import arccos, sqrt


def w_state():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    
    prog = pq.QProg()
    prog.insert(pq.RY(qubits[0], 2 * arccos(1 / sqrt(3))))
    prog.insert(pq.CH(qubits[0], qubits[1]))
    prog.insert(pq.CNOT(qubits[1], qubits[2]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.X(qubits[0]))
    
    # Measure all qubits
    cbits = machine.cAlloc_many(3)
    for i in range(3):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    
    machine.finalize()
    return prog
