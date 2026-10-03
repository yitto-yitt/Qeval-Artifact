# EVAL_META: task_id=78, framework=qpanda2, class=3
import atexit
import math
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)
atexit.register(machine.finalize)


def qft_no_swaps(num_qubits):
    num_qubits = operator.index(num_qubits)
    if num_qubits < 0:
        raise ValueError("num_qubits must be nonnegative")

    while len(qubits) < num_qubits:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    for j in range(num_qubits):
        for k in range(j):
            angle = -math.pi / (2 ** (j - k))
            circuit << pq.U1(qubits[k], angle).control([qubits[j]])
        circuit << pq.H(qubits[j])

    if num_qubits:
        program = pq.QProg()
        program << circuit
        machine.directly_run(program)

    return circuit
