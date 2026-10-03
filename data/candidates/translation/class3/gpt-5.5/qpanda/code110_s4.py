# EVAL_META: task_id=110, framework=qpanda, class=3
import random
import copy as _py_copy
import pyqpanda3.core as pq
from pyqpanda3.core import *

def equivalent_clifford_circuit(circuit, n):
    def _append(container, item):
        if item is None:
            return container, False
        for method_name in ("insert", "append", "push_back"):
            method = getattr(container, method_name, None)
            if callable(method):
                try:
                    ret = method(item)
                    return (container if ret is None else ret), True
                except Exception:
                    pass
        try:
            ret = container << item
            return (container if ret is None else ret), True
        except Exception:
            return container, False

    def _as_list(obj):
        if obj is None:
            return []
        try:
            return list(obj)
        except Exception:
            pass
        try:
            return [obj[i] for i in range(len(obj))]
        except Exception:
            return []

    def _get_qubits(obj):
        for func_name in (
            "get_all_used_qubits",
            "get_used_qubits",
            "get_qvec",
            "get_qubits",
            "get_used_qbits",
        ):
            func = getattr(pq, func_name, None)
            if callable(func):
                try:
                    qs = _as_list(func(obj))
                    if qs:
                        return qs
                except Exception:
                    pass

        for attr_name in (
            "get_used_qubits",
            "get_used_qbits",
            "get_qvec",
            "get_qubits",
            "qubits",
            "qbits",
        ):
            try:
                attr = getattr(obj, attr_name, None)
                if attr is None:
                    continue
                value = attr() if callable(attr) else attr
                qs = _as_list(value)
                if qs:
                    return qs
            except Exception:
                pass
        return []

    def _copy_circuit(obj):
        for method_name in ("copy", "clone"):
            method = getattr(obj, method_name, None)
            if callable(method):
                try:
                    return method()
                except Exception:
                    pass

        try:
            return _py_copy.copy(obj)
        except Exception:
            pass

        for cls in (obj.__class__, getattr(pq, "QCircuit", None), getattr(pq, "QProg", None)):
            if cls is None:
                continue
            try:
                new_obj = cls()
                new_obj, ok = _append(new_obj, obj)
                if ok:
                    return new_obj
            except Exception:
                pass

        return obj

    def _make_gate(name, *args):
        gate_func = getattr(pq, name, None)
        if callable(gate_func):
            try:
                return gate_func(*args)
            except Exception:
                return None
        return None

    def _add_random_identity(obj, qubits):
        if not qubits:
            return obj

        blocks = random.randint(1, 6)
        for _ in range(blocks):
            use_two = len(qubits) >= 2 and random.random() < 0.35
            if use_two:
                q0, q1 = random.sample(qubits, 2)
                gate_name = "CNOT" if callable(getattr(pq, "CNOT", None)) else "CX"
                gate1 = _make_gate(gate_name, q0, q1)
                gate2 = _make_gate(gate_name, q0, q1)
                if gate1 is not None and gate2 is not None:
                    obj, _ = _append(obj, gate1)
                    obj, _ = _append(obj, gate2)
                    continue

            q = random.choice(qubits)
            gate_name = random.choice(("H", "X", "Y", "Z"))
            gate1 = _make_gate(gate_name, q)
            gate2 = _make_gate(gate_name, q)
            if gate1 is not None and gate2 is not None:
                obj, _ = _append(obj, gate1)
                obj, _ = _append(obj, gate2)

        return obj

    qubits = _get_qubits(circuit)
    qc_list = []
    counter = 0
    while counter < n:
        qc = _copy_circuit(circuit)
        qc = _add_random_identity(qc, qubits)
        qc_list.append(qc)
        counter += 1
    return qc_list
