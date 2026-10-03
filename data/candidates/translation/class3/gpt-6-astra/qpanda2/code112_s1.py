# EVAL_META: task_id=112, framework=qpanda2, class=3
import atexit
import math
import pyqpanda as pq

machine = pq.CPUQVM()
machine.set_configure(64, 64)
machine.init_qvm()
qubits = machine.qAlloc_many(64)
atexit.register(machine.finalize)


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    if n > len(qubits):
        raise ValueError("The circuit exceeds the allocated qubit capacity.")
    if not isinstance(reps, int) or reps <= 0:
        raise ValueError("reps must be a positive integer.")

    circuit = pq.QCircuit()
    for qubit in qubits[:n]:
        circuit << pq.I(qubit)

    for pauli_string, time in zip(pauli_strings, times):
        sign = 1
        label = pauli_string
        if label.startswith("-"):
            sign = -1
            label = label[1:]
        elif label.startswith("+"):
            label = label[1:]

        if not label or any(char not in "IXYZ" for char in label):
            raise ValueError("Expected a Hermitian Pauli string.")
        if len(pauli_string) > n:
            raise ValueError("The Pauli string exceeds the circuit width.")

        active = [
            (index, char)
            for index, char in enumerate(reversed(label))
            if char != "I"
        ]
        step = sign * float(time) / reps

        for _ in range(reps):
            if not active:
                circuit << pq.U1(qubits[0], -step)
                circuit << pq.X(qubits[0])
                circuit << pq.U1(qubits[0], -step)
                circuit << pq.X(qubits[0])
                continue

            for index, char in active:
                if char == "X":
                    circuit << pq.H(qubits[index])
                elif char == "Y":
                    circuit << pq.RX(qubits[index], math.pi / 2)

            for left, right in zip(active, active[1:]):
                circuit << pq.CNOT(qubits[left[0]], qubits[right[0]])

            circuit << pq.RZ(qubits[active[-1][0]], 2 * step)

            for left, right in reversed(list(zip(active, active[1:]))):
                circuit << pq.CNOT(qubits[left[0]], qubits[right[0]])

            for index, char in reversed(active):
                if char == "X":
                    circuit << pq.H(qubits[index])
                elif char == "Y":
                    circuit << pq.RX(qubits[index], -math.pi / 2)

    program = pq.QProg()
    program << circuit
    pq.get_matrix(program)
    return circuit
