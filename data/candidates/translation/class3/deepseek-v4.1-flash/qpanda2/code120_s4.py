# EVAL_META: task_id=120, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    n = len(diag).bit_length() - 1
    mat = np.diag(diag).astype(np.complex128)
    gate = QGate(qubits[:n][::-1], mat)
    circ = QCircuit()
    circ << gate
    return circ

if __name__ == "__main__":
    machine.finalize()
