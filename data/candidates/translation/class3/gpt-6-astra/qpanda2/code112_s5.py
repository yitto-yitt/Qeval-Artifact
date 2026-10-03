# EVAL_META: task_id=112, framework=qpanda2, class=3
import atexit
import math
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = list(machine.qAlloc_many(1))
atexit.register(lambda: machine.finalize())


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()

    for pauli_string, time in zip(pauli_strings, times):
        label = pauli_string
        sign = 1.0
        if label.startswith("-"):
            sign = -1.0
            label = label[1:]
        elif label.startswith("+"):
            label = label[1:]

        if label.startswith("i"):
            raise ValueError("Pauli evolution requires a Hermitian operator.")
        if not label or any(p not in "IXYZ" for p in label):
            raise ValueError("Invalid Pauli string.")

        theta = sign * float(time) / reps
        active = [
            (index, pauli)
            for index, pauli in enumerate(reversed(label))
            if pauli != "I"
        ]

        for _ in range(reps):
            if not active:
                circuit << pq.RZ(qubits[0], 2.0 * theta)
                circuit << pq.U1(qubits[0], -2.0 * theta)
                continue

            for index, pauli in active:
                if pauli == "X":
                    circuit << pq.H(qubits[index])
                elif pauli == "Y":
                    circuit << pq.RX(qubits[index], math.pi / 2.0)

            for position in range(len(active) - 1):
                circuit << pq.CNOT(
                    qubits[active[position][0]],
                    qubits[active[position + 1][0]],
                )

            circuit << pq.RZ(qubits[active[-1][0]], 2.0 * theta)

            for position in reversed(range(len(active) - 1)):
                circuit << pq.CNOT(
                    qubits[active[position][0]],
                    qubits[active[position + 1][0]],
                )

            for index, pauli in reversed(active):
                if pauli == "X":
                    circuit << pq.H(qubits[index])
                elif pauli == "Y":
                    circuit << pq.RX(qubits[index], -math.pi / 2.0)

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
