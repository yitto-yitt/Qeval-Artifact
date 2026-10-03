# EVAL_META: task_id=112, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(29)
atexit.register(lambda: machine.finalize())

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    if n > len(q):
        raise ValueError("Not enough globally allocated qubits for the Pauli string length.")
    reps_count = int(reps)
    if reps_count <= 0:
        raise ValueError("reps must be a positive integer.")

    qc = QCircuit()

    for pauli_string, time in zip(pauli_strings, times):
        pstr = str(pauli_string).upper()
        theta = float(time) / reps_count

        for _ in range(reps_count):
            active_qubits = []

            for idx, pauli in enumerate(pstr):
                qb = q[n - 1 - idx]
                if pauli == "X":
                    qc << H(qb)
                    active_qubits.append(qb)
                elif pauli == "Y":
                    qc << RX(qb, math.pi / 2)
                    active_qubits.append(qb)
                elif pauli == "Z":
                    active_qubits.append(qb)
                elif pauli == "I":
                    continue
                else:
                    raise ValueError("Invalid Pauli character.")

            if len(active_qubits) == 1:
                qc << RZ(active_qubits[0], 2.0 * theta)
            elif len(active_qubits) > 1:
                target = active_qubits[-1]
                for control in active_qubits[:-1]:
                    qc << CNOT(control, target)
                qc << RZ(target, 2.0 * theta)
                for control in reversed(active_qubits[:-1]):
                    qc << CNOT(control, target)

            for idx in range(n - 1, -1, -1):
                pauli = pstr[idx]
                qb = q[n - 1 - idx]
                if pauli == "X":
                    qc << H(qb)
                elif pauli == "Y":
                    qc << RX(qb, -math.pi / 2)

    return qc
