# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import *
import math
import cmath


def create_diagonal_circuit(diag):
    size = len(diag)
    if size < 1 or (size & (size - 1)) != 0:
        raise ValueError("The length of diag must be a positive power of 2.")

    n = int(math.log2(size))
    qubits = list(range(n))

    def _new_circuit():
        cls = globals().get("QCircuit", None) or globals().get("Circuit", None) or globals().get("QProg", None)
        if cls is None:
            raise RuntimeError("No circuit/program container is available in pyqpanda3.core.")
        return cls()

    def _append(container, op):
        try:
            return container << op
        except Exception:
            if hasattr(container, "insert"):
                ret = container.insert(op)
                return container if ret is None else ret
            raise

    flat = [0j] * (size * size)
    for i, v in enumerate(diag):
        flat[i * size + i] = complex(v)
    nested = [[flat[r * size + c] for c in range(size)] for r in range(size)]

    matrix_candidates = []
    for m in (flat, nested):
        matrix_candidates.append(m)
        qstat = globals().get("QStat", None)
        if qstat is not None:
            try:
                matrix_candidates.append(qstat(m))
            except Exception:
                pass

    md = globals().get("matrix_decompose", None)
    if md is not None and n > 0:
        for m in matrix_candidates:
            for args in ((qubits, m), (m, qubits)):
                try:
                    return md(*args)
                except Exception:
                    pass

    for name in (
        "QOracle",
        "Oracle",
        "OracleGate",
        "MatrixGate",
        "Unitary",
        "UnitaryGate",
        "QUnitary",
        "QGate",
        "U",
    ):
        ctor = globals().get(name, None)
        if ctor is None or n == 0:
            continue
        for m in matrix_candidates:
            for args in (
                (qubits, m),
                (m, qubits),
                (qubits, m, "diagonal"),
                (m, qubits, "diagonal"),
            ):
                try:
                    gate = ctor(*args)
                    circ = _new_circuit()
                    return _append(circ, gate)
                except Exception:
                    pass

    circ = _new_circuit()
    if n == 0:
        return circ

    phases = [cmath.phase(complex(v)) for v in diag]
    coeff = phases[:]
    h = 1
    while h < size:
        step = h * 2
        for i in range(0, size, step):
            for j in range(h):
                x = coeff[i + j]
                y = coeff[i + j + h]
                coeff[i + j] = x + y
                coeff[i + j + h] = x - y
        h = step
    coeff = [x / size for x in coeff]

    for mask in range(1, size):
        angle = -2.0 * coeff[mask]
        if abs(angle) < 1e-12:
            continue
        target = (mask & -mask).bit_length() - 1
        controls = [i for i in range(n) if ((mask >> i) & 1) and i != target]
        for c in controls:
            circ = _append(circ, CNOT(qubits[c], qubits[target]))
        circ = _append(circ, RZ(qubits[target], angle))
        for c in reversed(controls):
            circ = _append(circ, CNOT(qubits[c], qubits[target]))

    return circ
