# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *
import math
import cmath
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    pauli_string = str(pauli_string).upper()
    n = len(pauli_string)

    machine = CPUQVM()
    for init_name in ("init_qvm", "init"):
        init_func = getattr(machine, init_name, None)
        if callable(init_func):
            try:
                init_func()
                break
            except TypeError:
                pass
            except RuntimeError:
                pass

    alloc_func = getattr(machine, "qAlloc_many", None)
    if alloc_func is None:
        alloc_func = getattr(machine, "qalloc_many", None)
    qubits = alloc_func(n) if n > 0 else []

    if not hasattr(synthesize_evolution_gate, "_machines"):
        synthesize_evolution_gate._machines = []
    synthesize_evolution_gate._machines.append(machine)

    circuit = QCircuit()

    identity_gate = globals().get("I", None)
    if callable(identity_gate):
        for qb in qubits:
            circuit << identity_gate(qb)

    if n == 0:
        return circuit

    labels = [pauli_string[n - 1 - i] for i in range(n)]
    active = [i for i, p in enumerate(labels) if p != "I"]

    if not active:
        phase = cmath.exp(-1j * float(time))
        mat = np.array([[phase, 0.0], [0.0, phase]], dtype=complex)
        oracle = globals().get("QOracle", None)
        if callable(oracle):
            try:
                circuit << oracle([qubits[0]], mat)
                return circuit
            except Exception:
                try:
                    circuit << oracle(qubits[0:1], mat.tolist())
                    return circuit
                except Exception:
                    pass
        return circuit

    for i in active:
        p = labels[i]
        if p == "X":
            circuit << H(qubits[i])
        elif p == "Y":
            circuit << RX(qubits[i], math.pi / 2.0)

    target = active[-1]
    cnot_gate = globals().get("CNOT", None)
    if cnot_gate is None:
        cnot_gate = globals().get("CX", None)

    for i in active[:-1]:
        circuit << cnot_gate(qubits[i], qubits[target])

    circuit << RZ(qubits[target], 2.0 * float(time))

    for i in reversed(active[:-1]):
        circuit << cnot_gate(qubits[i], qubits[target])

    for i in reversed(active):
        p = labels[i]
        if p == "X":
            circuit << H(qubits[i])
        elif p == "Y":
            circuit << RX(qubits[i], -math.pi / 2.0)

    return circuit
