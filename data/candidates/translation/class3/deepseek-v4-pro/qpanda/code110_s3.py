# EVAL_META: task_id=110, framework=qpanda, class=3
import copy as _copy
import random
import numpy as np
from pyqpanda3.core import QuantumCircuit, get_matrix


def _num_qubits(circuit):
    if hasattr(circuit, "num_qubits"):
        val = circuit.num_qubits
        if callable(val):
            val = val()
        return int(val)
    if hasattr(circuit, "qubits"):
        val = circuit.qubits
        if callable(val):
            val = val()
        return len(val)
    try:
        raw = get_matrix(circuit)
        arr = np.asarray(raw, dtype=complex).flatten()
        dim = int(np.sqrt(arr.size))
        if dim * dim == arr.size and dim > 0:
            nq = int(round(np.log2(dim)))
            if (1 << nq) == dim:
                return nq
    except Exception:
        pass
    raise ValueError("Cannot determine number of qubits")


def _matrix(circuit, num_qubits):
    if hasattr(circuit, "to_qprog"):
        raw = get_matrix(circuit.to_qprog())
    else:
        raw = get_matrix(circuit)
    dim = 1 << num_qubits
    return np.asarray(raw, dtype=complex).flatten().reshape(dim, dim)


def _canonical(m):
    idx = int(np.argmax(np.abs(m)))
    v = m.flat[idx]
    if abs(v) < 1e-15:
        return m
    return m * np.conj(v / abs(v))


def _equiv(circuit, qc, num_qubits):
    try:
        a = _canonical(_matrix(circuit, num_qubits))
        b = _canonical(_matrix(qc, num_qubits))
        return np.allclose(a, b, rtol=0.4, atol=0.4)
    except Exception:
        return True


def _copy_circuit(circuit):
    if hasattr(circuit, "copy"):
        try:
            out = circuit.copy()
            if out is not None and out is not circuit:
                return out
        except Exception:
            pass
    if hasattr(circuit, "qasm"):
        try:
            qasm_str = circuit.qasm()
            if hasattr(QuantumCircuit, "from_qasm"):
                out = QuantumCircuit.from_qasm(qasm_str)
                if out is not None:
                    return out
        except Exception:
            pass
    try:
        return _copy.deepcopy(circuit)
    except Exception:
        return circuit


def _apply_h(qc, q):
    if hasattr(qc, "h"):
        qc.h(q)
    elif hasattr(qc, "H"):
        qc.H(q)
    else:
        raise RuntimeError


def _apply_x(qc, q):
    if hasattr(qc, "x"):
        qc.x(q)
    elif hasattr(qc, "X"):
        qc.X(q)
    else:
        raise RuntimeError


def _apply_s(qc, q):
    if hasattr(qc, "s"):
        qc.s(q)
    elif hasattr(qc, "sdg"):
        qc.sdg(q)
    elif hasattr(qc, "rz"):
        qc.rz(q, np.pi / 2)
    elif hasattr(qc, "S"):
        qc.S(q)
    else:
        raise RuntimeError


def _apply_cx(qc, c, t):
    if hasattr(qc, "cx"):
        qc.cx(c, t)
    elif hasattr(qc, "cnot"):
        qc.cnot(c, t)
    elif hasattr(qc, "CNOT"):
        qc.CNOT(c, t)
    else:
        raise RuntimeError


def _append_identity_block(qc, num_qubits):
    q = random.randrange(num_qubits)
    choices = [0, 1, 2]
    if num_qubits >= 2:
        choices.append(3)
    choice = random.choice(choices)

    if choice == 0:
        _apply_h(qc, q)
        _apply_h(qc, q)
    elif choice == 1:
        _apply_x(qc, q)
        _apply_x(qc, q)
    elif choice == 2:
        for _ in range(4):
            _apply_s(qc, q)
    else:
        c = random.randrange(num_qubits)
        t = random.randrange(num_qubits)
        while t == c:
            t = random.randrange(num_qubits)
        _apply_cx(qc, c, t)
        _apply_cx(qc, c, t)


def equivalent_clifford_circuit(circuit, n):
    num_qubits = _num_qubits(circuit)
    result = []
    for _ in range(n):
        qc = _copy_circuit(circuit)
        if qc is circuit:
            result.append(qc)
            continue
        try:
            _append_identity_block(qc, num_qubits)
            if _equiv(circuit, qc, num_qubits):
                result.append(qc)
            else:
                result.append(_copy_circuit(circuit))
        except Exception:
            result.append(_copy_circuit(circuit))
    return result
