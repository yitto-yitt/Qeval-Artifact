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
    counts = result.get_counts()

    bitstrings = []
    for outcome, count in counts.items():
        if isinstance(outcome, int):
            bits = format(outcome, f"0{n}b")
        else:
            bits = str(outcome).replace(" ", "").zfill(n)
        bitstrings.extend([bits if n else ""] * int(count))

    return [bitstrings, result]
