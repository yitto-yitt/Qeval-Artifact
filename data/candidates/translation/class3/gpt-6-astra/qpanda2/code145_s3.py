# EVAL_META: task_id=145, framework=qpanda2, class=3
import atexit
import math
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)
atexit.register(lambda: machine.finalize())


def qft_inverse(n):
    n = operator.index(n)
    if n < 0:
        raise ValueError("The number of qubits must be nonnegative.")

    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()

    for j in range(n // 2):
        circuit << pq.SWAP(qubits[j], qubits[n - j - 1])

    for j in range(n):
        for k in range(j):
            angle = -math.pi / (2 ** (j - k))
            circuit << pq.U1(qubits[j], angle).control([qubits[k]])
        circuit << pq.H(qubits[j])

    if n:
        program = pq.QProg()
        program << circuit
        machine.directly_run(program)

    return circuit
