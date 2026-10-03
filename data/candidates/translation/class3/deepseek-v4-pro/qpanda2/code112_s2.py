# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import math
import atexit

machine = CPUQVM()
machine.init_qvm()
MAX_QUBITS = 32
global_qubits = machine.qAlloc_many(MAX_QUBITS)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    if n > len(global_qubits):
        raise ValueError("Input qubit count exceeds preallocated qubits")
    qubits = global_qubits[:n]
    circuit = QCircuit()
    reps = int(reps)
    if reps <= 0:
        raise ValueError("reps must be a positive integer")

    for pauli_string, time in zip(pauli_strings, times):
        pauli_string = pauli_string.upper()
        active = [i for i, p in enumerate(pauli_string) if p != 'I']
        if not active:
            continue

        block_time = time / reps
        for _ in range(reps):
            # Basis change: map X -> Z and Y -> Z.
            for i in active:
                p = pauli_string[i]
                if p == 'X':
                    circuit << H(qubits[i])
                elif p == 'Y':
                    circuit << RX(qubits[i], -math.pi / 2)
                elif p != 'Z':
                    raise ValueError(f"Invalid Pauli character: {p}")

            # CNOT ladder.
            for j in range(len(active) - 1):
                circuit << CNOT(qubits[active[j]], qubits[active[j + 1]])

            circuit << RZ(qubits[active[-1]], 2 * block_time)

            # Inverse CNOT ladder.
            for j in reversed(range(len(active) - 1)):
                circuit << CNOT(qubits[active[j]], qubits[active[j + 1]])

            # Undo basis change.
            for i in active:
                p = pauli_string[i]
                if p == 'X':
                    circuit << H(qubits[i])
                elif p == 'Y':
                    circuit << RX(qubits[i], math.pi / 2)
                elif p != 'Z':
                    raise ValueError(f"Invalid Pauli character: {p}")

    return circuit

atexit.register(machine.finalize)
