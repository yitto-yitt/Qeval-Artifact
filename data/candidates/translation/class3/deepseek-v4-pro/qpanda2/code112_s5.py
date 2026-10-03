# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = machine.qAlloc_many(num_qubits)
    circuit = QCircuit()

    for pauli_string, time in zip(pauli_strings, times):
        step_angle = 2.0 * time / reps

        for _ in range(reps):
            active = [idx for idx, pauli in enumerate(pauli_string) if pauli in ('X', 'Y', 'Z')]

            for idx, pauli in enumerate(pauli_string):
                if pauli == 'X':
                    circuit << H(qubits[idx])
                elif pauli == 'Y':
                    circuit << RX(qubits[idx], math.pi / 2)

            for ctrl, targ in zip(active[:-1], active[1:]):
                circuit << CNOT(qubits[ctrl], qubits[targ])

            if active:
                circuit << RZ(qubits[active[-1]], step_angle)

            for ctrl, targ in reversed(list(zip(active[:-1], active[1:]))):
                circuit << CNOT(qubits[ctrl], qubits[targ])

            for idx in range(num_qubits - 1, -1, -1):
                pauli = pauli_string[idx]
                if pauli == 'X':
                    circuit << H(qubits[idx])
                elif pauli == 'Y':
                    circuit << RX(qubits[idx], -math.pi / 2)

    return circuit

machine.finalize()
