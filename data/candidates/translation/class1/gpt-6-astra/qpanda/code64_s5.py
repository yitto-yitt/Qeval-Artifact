# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QProg, H, CNOT, measure


def simons_algorithm(s):
    n = len(s)
    reversed_s = s[::-1]
    circuit = QProg()

    for qubit in range(n):
        circuit << H(qubit)

    for qubit in range(n):
        circuit << CNOT(qubit, n + qubit)

    if "1" in reversed_s:
        control = reversed_s.find("1")
        for target, bit in enumerate(reversed_s):
            if bit == "1":
                circuit << CNOT(control, n + target)

        for qubit in range(n):
            circuit << H(qubit)

    for qubit in range(n):
        circuit << measure(qubit, qubit)

    return circuit
