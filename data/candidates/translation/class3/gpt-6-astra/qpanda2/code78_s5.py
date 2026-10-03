# EVAL_META: task_id=78, framework=qpanda2, class=3
import atexit
import operator
from math import pi
import pyqpanda as pq

machine = pq.CPUQVM()
machine.set_configure(64, 64)
machine.init_qvm()
qubits = machine.qAlloc_many(64)


def qft_no_swaps(num_qubits):
    num_qubits = operator.index(num_qubits)
    if not 0 <= num_qubits <= len(qubits):
        raise ValueError("num_qubits must be between 0 and 64")

    circuit = pq.QCircuit()
    for j in range(num_qubits):
        for k in range(j):
            circuit << pq.U1(
                qubits[k], -pi / (2 ** (j - k))
            ).control([qubits[j]])
        circuit << pq.H(qubits[j])
    return circuit


atexit.register(machine.finalize)
