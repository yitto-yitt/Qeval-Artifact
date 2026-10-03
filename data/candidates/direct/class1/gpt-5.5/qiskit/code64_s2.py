# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def simons_algorithm(s):
    n = len(s)
    secret = s[::-1]

    q = QuantumRegister(2 * n, "q")
    c = ClassicalRegister(n, "c")
    circuit = QuantumCircuit(q, c)

    for i in range(n):
        circuit.h(q[i])

    for i in range(n):
        circuit.cx(q[i], q[n + i])

    if "1" in secret:
        pivot = secret.find("1")
        for i, bit in enumerate(secret):
            if bit == "1":
                circuit.cx(q[pivot], q[n + i])

    for i in range(n):
        circuit.h(q[i])

    for i in range(n):
        circuit.measure(q[i], c[i])

    return circuit
