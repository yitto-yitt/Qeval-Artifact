# EVAL_META: task_id=71, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.H(qubits[1])
    prog << pq.CU1(qubits[0], qubits[1], np.pi / 2)
    prog << pq.H(qubits[1])
    return prog

machine.finalize()
