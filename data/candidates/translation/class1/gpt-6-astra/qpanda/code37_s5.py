# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, H, CNOT, measure


def bv_algorithm(s):
    n = len(s)
    ancilla = n
    prog = QProg()

    prog << X(ancilla)
    for qubit in range(n + 1):
        prog << H(qubit)

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(index, ancilla)

    for qubit in range(n):
        prog << H(qubit)
    for qubit in range(n):
        prog << measure(qubit, qubit)

    simulator = CPUQVM()
    simulator.run(prog, 1)
    result = simulator.result()
    bitstrings = [
        bitstring
        for bitstring, count in result.get_counts().items()
        for _ in range(int(count))
    ]
    return [bitstrings, result]
