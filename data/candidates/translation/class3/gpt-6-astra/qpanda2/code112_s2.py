# EVAL_META: task_id=112, framework=qpanda2, class=3
import atexit
import math
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(machine.finalize)


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    repetitions = operator.index(reps)
    if repetitions <= 0:
        raise ValueError("reps must be positive.")
    if n == 0:
        raise ValueError("Pauli strings must not be empty.")

    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()

    for pauli_string, time in zip(pauli_strings, times):
        if len(pauli_string) > n:
            raise ValueError("Pauli string exceeds the circuit width.")
        if any(label not in "IXYZ" for label in pauli_string):
            raise ValueError("Pauli strings must contain only I, X, Y, and Z.")

        step_time = float(time) / repetitions
        active = [
            (index, label)
            for index, label in enumerate(reversed(pauli_string))
            if label != "I"
        ]

        for _ in range(repetitions):
            if not active:
                circuit << pq.RZ(qubits[0], 2.0 * step_time)
                circuit << pq.U1(qubits[0], -2.0 * step_time)
                continue

            for index, label in active:
                if label == "X":
                    circuit << pq.H(qubits[index])
                elif label == "Y":
                    circuit << pq.RX(qubits[index], math.pi / 2.0)

            for position in range(len(active) - 1):
                control = active[position][0]
                target = active[position + 1][0]
                circuit << pq.CNOT(qubits[control], qubits[target])

            circuit << pq.RZ(qubits[active[-1][0]], 2.0 * step_time)

            for position in reversed(range(len(active) - 1)):
                control = active[position][0]
                target = active[position + 1][0]
                circuit << pq.CNOT(qubits[control], qubits[target])

            for index, label in reversed(active):
                if label == "X":
                    circuit << pq.H(qubits[index])
                elif label == "Y":
                    circuit << pq.RX(qubits[index], -math.pi / 2.0)

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
