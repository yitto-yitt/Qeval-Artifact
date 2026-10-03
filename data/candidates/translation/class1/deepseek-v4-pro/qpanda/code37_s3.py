# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QVM, QMachineType


def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    ancilla = n

    qc.x(ancilla)
    for i in range(n + 1):
        qc.h(i)

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, ancilla)

    for i in range(n):
        qc.h(i)

    for i in range(n):
        qc.measure(i, i)

    qvm = QVM(QMachineType.CPU)
    result = qvm.run(qc, shots=1)
    bitstrings = list(result.keys())
    return [bitstrings, result]
