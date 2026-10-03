# EVAL_META: task_id=112, framework=qpanda2, class=3
import atexit
import math
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
atexit.register(machine.finalize)


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    if n > len(qubits):
        raise ValueError("The circuit exceeds the allocated quantum register.")
    if not isinstance(reps, int) or reps <= 0:
        raise ValueError("reps must be a positive integer.")

    circuit = pq.QCircuit()
    for qubit in qubits[:n]:
        circuit << pq.I(qubit)

    for pauli_string, time in zip(pauli_strings, times):
        if len(pauli_string) > n:
            raise ValueError("A Pauli string exceeds the circuit width.")
        if any(symbol not in "IXYZ" for symbol in pauli_string):
            raise ValueError("Pauli strings must contain only I, X, Y, and Z.")

        operators = list(reversed(pauli_string))
        support = [
            index for index, symbol in enumerate(operators) if symbol != "I"
        ]
        angle = float(time) / reps

        for _ in range(reps):
            if not support:
                circuit << pq.RZ(qubits[0], 2.0 * angle)
                circuit << pq.U1(qubits[0], -2.0 * angle)
                continue

            for index in support:
                if operators[index] == "X":
                    circuit << pq.H(qubits[index])
                elif operators[index] == "Y":
                    circuit << pq.RX(qubits[index], math.pi / 2.0)

            edges = list(zip(support[:-1], support[1:]))
            for control, target in edges:
                circuit << pq.CNOT(qubits[control], qubits[target])

            circuit << pq.RZ(qubits[support[-1]], 2.0 * angle)

            for control, target in reversed(edges):
                circuit << pq.CNOT(qubits[control], qubits[target])

            for index in reversed(support):
                if operators[index] == "X":
                    circuit << pq.H(qubits[index])
                elif operators[index] == "Y":
                    circuit << pq.RX(qubits[index], -math.pi / 2.0)

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
