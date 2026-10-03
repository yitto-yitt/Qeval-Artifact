# EVAL_META: task_id=105, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def initialize_cnot_dihedral():
    circuit = pq.QCircuit()
    circuit << pq.CNOT(qubits[0], qubits[1])
    circuit << pq.T(qubits[0])
    return np.asarray(pq.get_matrix(circuit), dtype=complex).reshape(4, 4)


atexit.register(lambda: machine.finalize())
