# EVAL_META: task_id=112, framework=qpanda2, class=3
import atexit
import math
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    repetitions = operator.index(reps)
    if repetitions < 1:
        raise ValueError("reps must be a positive integer.")

    while len(qubits) < num_qubits:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()

    for pauli_string, time in zip(pauli_strings, times):
        if len(pauli_string) > num_qubits:
            raise ValueError("Pauli string exceeds the circuit width.")
        if any(pauli not in "IXYZ" for pauli in pauli_string):
            raise ValueError("Pauli strings must contain only I, X, Y, and Z.")

        active = [
            (index, pauli)
            for index, pauli in enumerate(reversed(pauli_string))
            if pauli != "I"
        ]
        step_time = float(time) / repetitions

        for _ in range(repetitions):
            if not active:
                circuit << pq.U1(qubits[0], -step_time)
                circuit << pq.X(qubits[0])
                circuit << pq.U1(qubits[0], -step_time)
                circuit << pq.X(qubits[0])
                continue

            for index, pauli in active:
                if pauli == "X":
                    circuit << pq.H(qubits[index])
                elif pauli == "Y":
                    circuit << pq.RX(qubits[index], math.pi / 2)

            for position in range(len(active) - 1):
                control = qubits[active[position][0]]
                target = qubits[active[position + 1][0]]
                circuit << pq.CNOT(control, target)

            circuit << pq.RZ(qubits[active[-1][0]], 2 * step_time)

            for position in reversed(range(len(active) - 1)):
                control = qubits[active[position][0]]
                target = qubits[active[position + 1][0]]
                circuit << pq.CNOT(control, target)

            for index, pauli in reversed(active):
                if pauli == "X":
                    circuit << pq.H(qubits[index])
                elif pauli == "Y":
                    circuit << pq.RX(qubits[index], -math.pi / 2)

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(lambda: machine.finalize())
