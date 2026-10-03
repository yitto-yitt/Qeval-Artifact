# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QuantumMachine


def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit()

    try:
        qubits = qc.allocate_qubits(n + 1)
        cbits = qc.allocate_cbits(n)
    except AttributeError:
        qubits = qc.qAlloc_many(n + 1)
        cbits = qc.cAlloc_many(n)

    ancilla = n

    qc.x(qubits[ancilla])
    for i in range(n + 1):
        qc.h(qubits[i])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cnot(qubits[index], qubits[ancilla])

    for i in range(n):
        qc.h(qubits[i])

    for i in range(n):
        qc.measure(qubits[i], cbits[i])

    machine = QuantumMachine()
    result = machine.run(qc, shots=1)

    if isinstance(result, dict):
        bitstrings = list(result.keys())
    else:
        bitstrings = list(result.get_counts().keys())

    return [bitstrings, result]
