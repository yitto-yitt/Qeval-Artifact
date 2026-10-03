# EVAL_META: task_id=65, framework=qpanda2, class=3
import atexit
from operator import index
from numpy import pi
import pyqpanda as pq

machine = pq.CPUQVM()
machine.set_configure(64, 64)
machine.init_qvm()
qubits = machine.qAlloc_many(64)
atexit.register(machine.finalize)


def QFT(n):
    n = index(n)
    if not 0 <= n <= len(qubits):
        raise ValueError("n must be between 0 and 64")

    circuit = pq.QCircuit()

    for target in range(n - 1, -1, -1):
        circuit << pq.H(qubits[target])
        for control in range(target):
            angle = pi / (2 ** (target - control))
            circuit << pq.U1(qubits[target], angle).control([qubits[control]])

    for i in range(n // 2):
        circuit << pq.SWAP(qubits[i], qubits[n - i - 1])

    if n:
        program = pq.QProg()
        program << circuit
        pq.get_matrix(program)

    return circuit
