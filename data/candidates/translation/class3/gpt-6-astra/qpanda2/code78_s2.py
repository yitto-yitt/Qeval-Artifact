# EVAL_META: task_id=78, framework=qpanda2, class=3
import atexit
import math
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(machine.finalize)


def qft_no_swaps(num_qubits):
    num_qubits = operator.index(num_qubits)
    if num_qubits < 0:
        raise ValueError("num_qubits must be nonnegative")

    while len(qubits) < num_qubits:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    for target in range(num_qubits):
        for control in range(target):
            angle = -math.pi / (2 ** (target - control))
            circuit << pq.CR(qubits[control], qubits[target], angle)
        circuit << pq.H(qubits[target])

    return circuit
