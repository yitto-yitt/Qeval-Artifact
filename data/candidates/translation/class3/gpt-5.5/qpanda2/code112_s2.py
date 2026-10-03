# EVAL_META: task_id=112, framework=qpanda2, class=3
import atexit
import math
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
atexit.register(machine.finalize)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    circuit = QCircuit()
    if not pauli_strings:
        return circuit

    n = len(pauli_strings[0])
    if n > len(qubits):
        raise ValueError("Not enough globally allocated qubits for the requested Pauli string length.")

    reps = int(reps)

    for pauli_string, time in zip(pauli_strings, times):
        dt = float(time) / reps
        angle = 2.0 * dt

        for _ in range(reps):
            active = []

            for idx, p in enumerate(pauli_string):
                qidx = n - 1 - idx
                if p == "X":
                    circuit.insert(H(qubits[qidx]))
                    active.append(qidx)
                elif p == "Y":
                    circuit.insert(RZ(qubits[qidx], -math.pi / 2.0))
                    circuit.insert(H(qubits[qidx]))
                    active.append(qidx)
                elif p == "Z":
                    active.append(qidx)

            if len(active) == 1:
                circuit.insert(RZ(qubits[active[0]], angle))
            elif len(active) > 1:
                for i in range(len(active) - 1):
                    circuit.insert(CNOT(qubits[active[i]], qubits[active[i + 1]]))
                circuit.insert(RZ(qubits[active[-1]], angle))
                for i in range(len(active) - 2, -1, -1):
                    circuit.insert(CNOT(qubits[active[i]], qubits[active[i + 1]]))

            for idx in range(len(pauli_string) - 1, -1, -1):
                p = pauli_string[idx]
                qidx = n - 1 - idx
                if p == "X":
                    circuit.insert(H(qubits[qidx]))
                elif p == "Y":
                    circuit.insert(H(qubits[qidx]))
                    circuit.insert(RZ(qubits[qidx], math.pi / 2.0))

    return circuit
