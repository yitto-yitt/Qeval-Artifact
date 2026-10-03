# EVAL_META: task_id=66, framework=qpanda2, class=2
import pyqpanda as pq
import numpy as np

def w_state():
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = pq.QProg()
    
    theta = 2 * np.arccos(1 / np.sqrt(3))
    prog << pq.RY(qubits[0], theta)
    
    prog << pq.CZ(qubits[0], qubits[1])
    prog << pq.CRY(qubits[0], qubits[1], np.pi / 2)
    
    prog << pq.CNOT(qubits[1], qubits[2])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.X(qubits[0])
    
    prog << pq.measure_all(qubits, cbits)
    
    return prog
