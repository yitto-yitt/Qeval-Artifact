# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import random

def equivalent_clifford_circuit(circuit, n):
    def _as_list(q):
        if q is None:
            return []
        if isinstance(q, (list, tuple, set)):
            return list(q)
        try:
            return list(q)
        except TypeError:
            return [q]

    def _get_qubits(c):
        for name in ('get_used_qubits', 'get_qubits', 'getUsedQubits'):
            if hasattr(c, name):
                try:
                    qubits = _as_list(getattr(c, name)())
                    if qubits:
                        return qubits
                except Exception:
                    pass
        if hasattr(c, 'qubits'):
            try:
                qubits = _as_list(c.qubits)
                if qubits:
                    return qubits
            except Exception:
                pass
        return []

    def _new_container_like(c):
        try:
            if isinstance(c, QProg):
                return QProg()
        except NameError:
            pass
        return QCircuit()

    def _insert(target, node):
        try:
            target.insert(node)
            return
        except Exception:
            pass
        try:
            target.push_back(node)
        except Exception:
            pass

    def _append_circuit_content(target, source):
        try:
            for node in source:
                _insert(target, node)
            return
        except Exception:
            pass
        for name in ('get_gates', 'get_qgates', 'get_gate_list'):
            if hasattr(source, name):
                try:
                    for node in getattr(source, name)():
                        _insert(target, node)
                    return
                except Exception:
                    pass
        try:
            _insert(target, source)
        except Exception:
            pass

    def _copy_circuit(c):
        for name in ('copy', 'clone'):
            if hasattr(c, name):
                try:
                    copied = getattr(c, name)()
                    if copied is not None:
                        return copied
                except Exception:
                    pass
        try:
            return type(c)(c)
        except Exception:
            pass
        try:
            return QCircuit(c)
        except Exception:
            pass
        target = _new_container_like(c)
        _append_circuit_content(target, c)
        return target

    def _make_gates(spec, qubits):
        if len(spec) == 3:
            _, a, b = spec
            return [CNOT(qubits[a], qubits[b])]
        t = spec[0]
        a = spec[1]
        if t == 'H':
            return [H(qubits[a])]
        return [X(qubits[a])]

    def _random_spec(qubits):
        m = len(qubits)
        choices = ['H', 'X']
        if m >= 2:
            choices.append('CNOT')
        t = random.choice(choices)
        if t == 'CNOT':
            a = random.randrange(m)
            b = random.randrange(m - 1)
            if b >= a:
                b += 1
            return ('CNOT', a, b)
        return (t, random.randrange(m))

    qubits = _get_qubits(circuit)
    qc_list = []

    if not qubits:
        for _ in range(n):
            qc_list.append(_copy_circuit(circuit))
        return qc_list

    for _ in range(n):
        qc = _copy_circuit(circuit)
        specs = []
        length = random.randint(1, max(1, 5 * len(qubits)))
        for _ in range(length):
            spec = _random_spec(qubits)
            specs.append(spec)
            for gate in _make_gates(spec, qubits):
                _insert(qc, gate)
        for spec in reversed(specs):
            for gate in _make_gates(spec, qubits):
                _insert(qc, gate)
        qc_list.append(qc)

    return qc_list
