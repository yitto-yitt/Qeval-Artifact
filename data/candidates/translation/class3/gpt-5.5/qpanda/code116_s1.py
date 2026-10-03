# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *
import math

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    try:
        qc = QCircuit(n)
    except TypeError:
        qc = QCircuit()

    paulis_by_qubit = list(reversed(pauli_string))
    active = [i for i, p in enumerate(paulis_by_qubit) if p != "I"]

    for q in range(n):
        if paulis_by_qubit[q] == "I":
            try:
                qc << I(q)
            except Exception:
                pass

    if not active:
        for name in ("set_global_phase", "setGlobalPhase"):
            try:
                getattr(qc, name)(-float(time))
                return qc
            except Exception:
                pass
        try:
            qc.global_phase = -float(time)
        except Exception:
            pass
        return qc

    for q in active:
        p = paulis_by_qubit[q]
        if p == "X":
            qc << H(q)
        elif p == "Y":
            qc << RX(q, math.pi / 2)

    target = active[-1]
    for q in active[:-1]:
        qc << CNOT(q, target)

    qc << RZ(target, 2 * float(time))

    for q in reversed(active[:-1]):
        qc << CNOT(q, target)

    for q in reversed(active):
        p = paulis_by_qubit[q]
        if p == "X":
            qc << H(q)
        elif p == "Y":
            qc << RX(q, -math.pi / 2)

    return qc
