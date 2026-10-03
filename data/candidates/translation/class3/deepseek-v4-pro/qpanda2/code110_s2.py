# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import random

qvm = CPUQVM()
qvm.init_qvm()
q_pool = qvm.qAlloc_many(32)


def _to_list(q):
    if q is None:
        return None
    try:
        return list(q)
    except Exception:
        pass
    try:
        return [q[i] for i in range(len(q))]
    except Exception:
        return None


def _get_qubits(circuit):
    try:
        qubits = _to_list(get_used_qubits(circuit))
        if qubits:
            return qubits
    except Exception:
        pass

    try:
        qubits = _to_list(circuit.get_qubits())
        if qubits:
            return qubits
    except Exception:
        pass

    try:
        qubits = _to_list(circuit.qubits)
        if qubits:
            return qubits
    except Exception:
        pass

    for attr in ('num_qubits', 'qubit_num'):
        try:
            val = getattr(circuit, attr)
            num = val() if callable(val) else val
            num = int(num)
            if 0 < num <= len(q_pool):
                return list(q_pool[:num])
        except Exception:
            pass

    return list(q_pool[:2])


def _append_gate(prog, kind, qs):
    if kind == 'H':
        prog << H(qs[0])
    elif kind == 'X':
        prog << X(qs[0])
    elif kind == 'Y':
        prog << Y(qs[0])
    elif kind == 'Z':
        prog << Z(qs[0])
    elif kind == 'CNOT':
        prog << CNOT(qs[0], qs[1])


def _random_self_inverse_gate(qubits):
    if len(qubits) == 1 or random.random() < 0.55:
        kind = random.choice(['H', 'X', 'Y', 'Z'])
        q = random.choice(qubits)
        return kind, [q]

    control = random.choice(qubits)
    target = random.choice(qubits)
    while target == control:
        target = random.choice(qubits)
    return 'CNOT', [control, target]


def _append_random_identity(prog, qubits):
    length = random.randint(1, max(1, len(qubits) * 2))
    seq = []
    for _ in range(length):
        gate = _random_self_inverse_gate(qubits)
        seq.append(gate)
        _append_gate(prog, gate[0], gate[1])

    for gate in reversed(seq):
        _append_gate(prog, gate[0], gate[1])


def equivalent_clifford_circuit(circuit, n):
    result = []
    for _ in range(n):
        prog = QProg()
        prog << circuit

        qubits = _get_qubits(circuit)
        if not qubits:
            qubits = _get_qubits(prog)
        if not qubits:
            qubits = list(q_pool[:2])

        _append_random_identity(prog, qubits)
        result.append(prog)

    return result


qvm.finalize()
