# EVAL_META: task_id=58, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init()
qubits = machine.qAlloc_many(2)

def create_ch_gate():
    circ = pq.RY(qubits[1], np.pi / 4) + pq.CNOT(qubits[0], qubits[1]) + pq.RY(qubits[1], -np.pi / 4)
    return circ

machine.finalize()
