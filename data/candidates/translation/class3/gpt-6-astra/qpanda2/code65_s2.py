# EVAL_META: task_id=65, framework=qpanda2, class=3
import atexit
from operator import index
from numpy import pi
from pyqpanda import CPUQVM, QCircuit, QProg, H, P, SWAP

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)
atexit.register(lambda: machine.finalize())


def QFT(n):
    n = index(n)
    if n < 0:
        raise ValueError("n must be nonnegative")

    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = QCircuit()

    for target in range(n - 1, -1, -1):
        circuit << H(qubits[target])
        for control in range(target):
            circuit << P(
                qubits[target], pi / 2 ** (target - control)
            ).control([qubits[control]])

    for qubit in range(n // 2):
        circuit << SWAP(qubits[qubit], qubits[n - qubit - 1])

    if n:
        program = QProg()
        program << circuit
        machine.directly_run(program)

    return circuit
