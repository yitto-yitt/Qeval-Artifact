# EVAL_META: task_id=65, framework=qpanda2, class=3
import atexit
import operator
from math import pi
from pyqpanda import CPUQVM, QCircuit, QProg, H, U1, SWAP, Reset

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)
atexit.register(machine.finalize)


def QFT(n):
    n = operator.index(n)
    if n < 0:
        raise ValueError("The number of qubits must be nonnegative.")

    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = QCircuit()
    for target in range(n - 1, -1, -1):
        circuit << H(qubits[target])
        for control in range(target):
            circuit << U1(
                qubits[target], pi / (2 ** (target - control))
            ).control([qubits[control]])

    for index in range(n // 2):
        circuit << SWAP(qubits[index], qubits[n - index - 1])

    if n:
        program = QProg()
        for qubit in qubits[:n]:
            program << Reset(qubit)
        program << circuit
        machine.directly_run(program)

    return circuit
