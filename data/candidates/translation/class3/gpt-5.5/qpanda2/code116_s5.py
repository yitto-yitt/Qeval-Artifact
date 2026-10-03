# EVAL_META: task_id=116, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
try:
    machine.set_configure(64, 64)
except Exception:
    pass
machine.init_qvm()
qubits = machine.qAlloc_many(64)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    if n > len(qubits):
        raise ValueError("Pauli string is longer than the globally allocated qubit register.")

    circuit = QCircuit()
    active = []

    for i, p in enumerate(pauli_string):
        qb = qubits[n - 1 - i]
        if p == "I":
            continue
        if p == "X":
            circuit << H(qb)
        elif p == "Y":
            circuit << RX(qb, math.pi / 2)
        elif p == "Z":
            pass
        else:
            raise ValueError("Pauli string can only contain 'I', 'X', 'Y', and 'Z'.")
        active.append((qb, p))

    if not active:
        if n > 0:
            circuit << U4(qubits[0], -time, 0.0, 0.0, 0.0)
        return circuit

    active_qubits = [item[0] for item in active]
    target = active_qubits[-1]

    for control in active_qubits[:-1]:
        circuit << CNOT(control, target)

    circuit << RZ(target, 2 * time)

    for control in reversed(active_qubits[:-1]):
        circuit << CNOT(control, target)

    for qb, p in reversed(active):
        if p == "X":
            circuit << H(qb)
        elif p == "Y":
            circuit << RX(qb, -math.pi / 2)

    return circuit

atexit.register(machine.finalize)
