# EVAL_META: task_id=120, framework=qpanda, class=3
import math
import cmath
import pyqpanda3.core as pq
from pyqpanda3.core import *

def create_diagonal_circuit(diag):
    diag = [complex(x) for x in diag]
    dim = len(diag)
    if dim == 0 or (dim & (dim - 1)) != 0:
        raise ValueError("Diagonal length must be a positive power of 2.")
    for z in diag:
        if abs(abs(z) - 1.0) > 1e-8:
            raise ValueError("Diagonal entries must have magnitude 1.")
    n = dim.bit_length() - 1

    def _new_prog():
        return pq.QProg()

    def _append(container, node):
        if node is None:
            return container
        if hasattr(container, "insert"):
            try:
                r = container.insert(node)
                return container if r is None else r
            except Exception:
                pass
        try:
            r = container << node
            return container if r is None else r
        except Exception:
            pass
        raise RuntimeError("Unable to append node to QProg.")

    def _alloc_qubits(count):
        machine = None
        for cls_name in ("CPUQVM", "CPUSingleThreadQVM"):
            cls = getattr(pq, cls_name, None)
            if cls is not None:
                try:
                    machine = cls()
                    break
                except Exception:
                    machine = None
        if machine is not None:
            for init_name in ("init_qvm", "init", "initialize"):
                if hasattr(machine, init_name):
                    try:
                        getattr(machine, init_name)()
                        break
                    except Exception:
                        pass
            for method_name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "allocate_qbits", "qAllocMany"):
                if hasattr(machine, method_name):
                    try:
                        qubits = getattr(machine, method_name)(count)
                        globals().setdefault("_TASK120_QPANDA_MACHINES", []).append(machine)
                        return qubits
                    except Exception:
                        pass
        for func_name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "allocate_qbits"):
            func = getattr(pq, func_name, None)
            if callable(func):
                try:
                    return func(count)
                except Exception:
                    pass
        raise RuntimeError("Unable to allocate qubits.")

    qubits = _alloc_qubits(n) if n else []
    prog = _new_prog()

    if n == 0:
        return prog

    matrix = [[0j for _ in range(dim)] for _ in range(dim)]
    for i, value in enumerate(diag):
        matrix[i][i] = value
    flat_matrix = [matrix[i][j] for i in range(dim) for j in range(dim)]

    for name in ("QOracle", "Oracle", "Unitary", "QUnitary"):
        obj = getattr(pq, name, None)
        if callable(obj):
            for mat in (matrix, flat_matrix):
                for args in ((qubits, mat), (mat, qubits)):
                    try:
                        trial_prog = _new_prog()
                        gate = obj(*args)
                        trial_prog = _append(trial_prog, gate)
                        return trial_prog
                    except Exception:
                        pass

    for name in ("matrix_decompose", "MatrixDecompose", "matrix_decomposition"):
        obj = getattr(pq, name, None)
        if callable(obj):
            for mat in (matrix, flat_matrix):
                for args in ((qubits, mat), (mat, qubits)):
                    try:
                        trial_prog = _new_prog()
                        circ = obj(*args)
                        trial_prog = _append(trial_prog, circ)
                        return trial_prog
                    except Exception:
                        pass

    def _gate(names, *args):
        for name in names:
            fn = getattr(pq, name, None)
            if callable(fn):
                try:
                    return fn(*args)
                except Exception:
                    pass
        raise RuntimeError("Required gate is unavailable.")

    def _cnot(control, target):
        return _gate(("CNOT", "CX"), control, target)

    def _rz(qubit, angle):
        return _gate(("RZ", "Rz", "rz"), qubit, angle)

    def _parity(x):
        return bin(x).count("1") & 1

    phases = [cmath.phase(z) for z in diag]

    for mask in range(1, dim):
        coeff = 0.0
        for basis in range(dim):
            coeff += phases[basis] * (-1 if _parity(basis & mask) else 1)
        coeff /= dim
        angle = -2.0 * coeff
        if abs(angle) < 1e-12:
            continue

        indices = [i for i in range(n) if (mask >> i) & 1]
        target = indices[-1]
        controls = indices[:-1]

        for control in controls:
            prog = _append(prog, _cnot(qubits[control], qubits[target]))
        prog = _append(prog, _rz(qubits[target], angle))
        for control in reversed(controls):
            prog = _append(prog, _cnot(qubits[control], qubits[target]))

    return prog
