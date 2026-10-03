# EVAL_META: task_id=65, framework=qpanda2, class=3
import atexit
from math import pi
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)


def QFT(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a nonnegative integer")

    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()

    for target in range(n - 1, -1, -1):
        circuit << pq.H(qubits[target])
        for control in range(target):
            angle = pi / (2 ** (target - control))
            circuit << pq.P(qubits[target], angle).control([qubits[control]])

    for index in range(n // 2):
        circuit << pq.SWAP(qubits[index], qubits[n - index - 1])

    if n:
        program = pq.QProg()
        for qubit in qubits:
            program << pq.Reset(qubit)
        program << circuit
        machine.directly_run(program)

    return circuit


atexit.register(lambda: machine.finalize())
