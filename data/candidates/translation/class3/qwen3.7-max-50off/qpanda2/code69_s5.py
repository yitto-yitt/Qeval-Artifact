# EVAL_META: task_id=69, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CP(qubits[0], qubits[1], np.pi / 2)
    prog << pq.H(qubits[1])
    prog << pq.CP(qubits[1], qubits[0], -np.pi / 2)
    return prog

machine.finalize()
