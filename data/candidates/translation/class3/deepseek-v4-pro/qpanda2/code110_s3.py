# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_GLOBAL_QUBITS = machine.qAlloc_many(32)


def _as_qubit_list(q):
    if q is None:
        return []
    try:
        return list(q)
    except TypeError:
        return [q[i] for i in range(len(q))]


def _get_qubits(circ):
    for name in ('get_qubits', 'get_used_qubits', 'get_qbits'):
        attr = getattr(circ, name, None)
        if attr is not None:
            if callable(attr):
                try:
                    qubits = _as_qubit_list(attr())
                except Exception:
                    continue
            else:
                qubits = _as_qubit_list(attr)
            if qubits:
                return qubits
    try:
        qubits = _as_qubit_list(get_used_qubits(circ))
        if qubits:
            return qubits
    except Exception:
        pass
    return []


def _append_gate(prog, desc, qubits):
    name = desc[0]
    if name == 'CNOT':
        prog << CNOT(qubits[desc[1]], qubits[desc[2]])
    elif name == 'H':
        prog << H(qubits[desc[1]])
    elif name == 'S':
        prog << S(qubits[desc[1]])
    elif name == 'X':
        prog << X(qubits[desc[1]])
    elif name == 'Y':
        prog << Y(qubits[desc[1]])
    elif name == 'Z':
        prog << Z(qubits[desc[1]])


def _append_inverse_gate(prog, desc, qubits):
    name = desc[0]
    if name == 'S':
        for _ in range(3):
            prog << S(qubits[desc[1]])
    else:
        _append_gate(prog, desc, qubits)


def _build_random_identity(num_qubits):
    if num_qubits == 0:
        return []
    depth = random.randint(num_qubits, max(num_qubits, 10 * num_qubits))
    descs = []
    for _ in range(depth):
        if num_qubits >= 2 and random.random() < 0.35:
            ctrl, tgt = random.sample(range(num_qubits), 2)
            descs.append(('CNOT', ctrl, tgt))
        else:
            gate_name = random.choice(['H', 'S', 'X', 'Y', 'Z'])
            descs.append((gate_name, random.randrange(num_qubits)))
    return descs


def _new_container(circuit):
    if isinstance(circuit, QCircuit):
        return QCircuit()
    return QProg()


def equivalent_clifford_circuit(circuit, n):
    qubits = _get_qubits(circuit)
    num_qubits = len(qubits)
    out_list = []

    for _ in range(n):
        out = _new_container(circuit)
        if num_qubits > 0:
            try:
                out << circuit
            except Exception:
                out.insert(circuit)

            descs = _build_random_identity(num_qubits)
            for desc in descs:
                _append_gate(out, desc, qubits)
            for desc in reversed(descs):
                _append_inverse_gate(out, desc, qubits)

        out_list.append(out)

    return out_list


machine.finalize()
