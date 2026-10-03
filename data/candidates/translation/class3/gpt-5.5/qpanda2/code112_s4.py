# EVAL_META: task_id=112, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import CPUQVM, QCircuit, H, RZ, CNOT

machine = CPUQVM()
machine.init_qvm()
qbits = machine.qAlloc_many(256)
atexit.register(machine.finalize)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    circuit = QCircuit()
    if not pauli_strings:
        return circuit

    n = len(pauli_strings[0])
    reps = int(reps)

    for pauli_string, time in zip(pauli_strings, times):
        dt = float(time) / reps

        for _ in range(reps):
            active = []
            pauli_by_qubit = {}

            for label_index, pauli_char in enumerate(pauli_string):
                q_index = n - 1 - label_index
                if pauli_char != "I":
                    active.append(q_index)
                    pauli_by_qubit[q_index] = pauli_char

            active.sort()

            for q_index in active:
                pauli_char = pauli_by_qubit[q_index]
                if pauli_char == "X":
                    circuit.insert(H(qbits[q_index]))
                elif pauli_char == "Y":
                    circuit.insert(RZ(qbits[q_index], -math.pi / 2))
                    circuit.insert(H(qbits[q_index]))

            if len(active) == 1:
                circuit.insert(RZ(qbits[active[0]], 2.0 * dt))
            elif len(active) > 1:
                for i in range(len(active) - 1):
                    circuit.insert(CNOT(qbits[active[i]], qbits[active[i + 1]]))

                circuit.insert(RZ(qbits[active[-1]], 2.0 * dt))

                for i in range(len(active) - 2, -1, -1):
                    circuit.insert(CNOT(qbits[active[i]], qbits[active[i + 1]]))

            for q_index in reversed(active):
                pauli_char = pauli_by_qubit[q_index]
                if pauli_char == "X":
                    circuit.insert(H(qbits[q_index]))
                elif pauli_char == "Y":
                    circuit.insert(H(qbits[q_index]))
                    circuit.insert(RZ(qbits[q_index], math.pi / 2))

    return circuit
