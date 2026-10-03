# EVAL_META: task_id=65, framework=qpanda2, class=3
import atexit
from math import pi
from operator import index
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)


def QFT(n):
    n = index(n)
    if n < 0:
        raise ValueError("n must be nonnegative")

    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    for target in range(n - 1, -1, -1):
        circuit << pq.H(qubits[target])
        for control in range(target):
            angle = pi / 2 ** (target - control)
            circuit << pq.U1(qubits[target], angle).control([qubits[control]])

    for qubit in range(n // 2):
        circuit << pq.SWAP(qubits[qubit], qubits[n - qubit - 1])

    if n:
        program = pq.QProg()
        program << circuit
        machine.directly_run(program)

    return circuit


atexit.register(lambda: machine.finalize())
