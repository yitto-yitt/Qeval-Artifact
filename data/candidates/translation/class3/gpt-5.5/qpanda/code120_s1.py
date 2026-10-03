# EVAL_META: task_id=120, framework=qpanda, class=3
import math
import numpy as np
from pyqpanda3.core import *

def create_diagonal_circuit(diag):
    size = len(diag)
    if size <= 0 or (size & (size - 1)) != 0:
        raise ValueError("diag length must be a positive power of 2")

    num_qubits = int(math.log2(size))

    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(num_qubits)
    elif hasattr(qvm, "qalloc_many"):
        qubits = qvm.qalloc_many(num_qubits)
    else:
        qubits = [qvm.qAlloc() for _ in range(num_qubits)]

    circuit = QCircuit()

    phases = [float(np.angle(x)) for x in diag]
    coeffs = phases[:]
    for bit in range(num_qubits):
        step = 1 << bit
        for mask in range(size):
            if mask & step:
                coeffs[mask] -= coeffs[mask ^ step]

    def _phase_gate(q, angle):
        if "P" in globals():
            return P(q, angle)
        if "U1" in globals():
            return U1(q, angle)
        if "Phase" in globals():
            return Phase(q, angle)
        if "QOracle" in globals():
            mat = np.diag(np.asarray(diag, dtype=complex))
            return QOracle(qubits, mat)
        raise RuntimeError("No phase-gate implementation available in pyqpanda3.core")

    for mask in range(1, size):
        angle = coeffs[mask]
        if abs(angle) < 1e-12:
            continue
        target = (mask & -mask).bit_length() - 1
        controls = [qubits[i] for i in range(num_qubits) if (mask & (1 << i)) and i != target]
        gate = _phase_gate(qubits[target], angle)
        if controls:
            gate = gate.control(controls)
        circuit << gate

    try:
        circuit._qvm = qvm
        circuit._qubits = qubits
    except Exception:
        pass

    return circuit
