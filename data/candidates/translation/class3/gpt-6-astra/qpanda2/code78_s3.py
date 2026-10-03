# EVAL_META: task_id=78, framework=qpanda2, class=3
import atexit
import math
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.set_configure(64, 64)
machine.init_qvm()
qubits = machine.qAlloc_many(64)
atexit.register(machine.finalize)


def qft_no_swaps(num_qubits):
    num_qubits = operator.index(num_qubits)
    if not 0 <= num_qubits <= len(qubits):
        raise ValueError("num_qubits must be between 0 and 64")

    circuit = pq.QCircuit()
    for target in range(num_qubits):
        for control in range(target):
            circuit << pq.CR(
                qubits[control],
                qubits[target],
                -math.pi / (2 ** (target - control)),
            )
        circuit << pq.H(qubits[target])

    if num_qubits:
        program = pq.QProg()
        program << circuit
        pq.get_matrix(program)

    return circuit
