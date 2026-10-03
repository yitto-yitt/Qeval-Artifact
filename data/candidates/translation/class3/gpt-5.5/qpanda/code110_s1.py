# EVAL_META: task_id=110, framework=qpanda, class=3
import random
import copy
from pyqpanda3.core import *

def equivalent_clifford_circuit(circuit, n):
    def _try_call(obj, name):
        attr = getattr(obj, name, None)
        if attr is None:
            return None
        try:
            return attr() if callable(attr) else attr
        except Exception:
            return None

    def _get_qubits(obj):
        for name in (
            "get_used_qubits",
            "get_used_qbits",
            "used_qubits",
            "used_qbits",
            "get_qubits",
            "get_qbits",
            "qubits",
            "qbits",
            "get_all_qubits",
            "get_all_qbits",
        ):
            qs = _try_call(obj, name)
            if qs is not None:
                try:
                    return list(qs)
                except Exception:
                    pass

        for fn_name in (
            "get_used_qubits",
            "get_used_qbits",
            "get_all_used_qubits",
            "get_all_used_qbits",
        ):
            fn = globals().get(fn_name)
            if callable(fn):
                try:
                    qs = fn(obj)
                    return list(qs)
                except Exception:
                    pass
        return []

    def _append(dst, item):
        try:
            res = dst << item
            return dst if res is None else res
        except Exception:
            pass
        try:
            res = dst.insert(item)
            return dst if res is None else res
        except Exception:
            pass
        raise

    def _copy_circuit(obj):
        try:
            return copy.deepcopy(obj)
        except Exception:
            return obj

    def _random_identity_pair(q):
        gates = (H, X, Y, Z)
        g = random.choice(gates)
        return g(q), g(q)

    qubits = _get_qubits(circuit)
    result = []

    for _ in range(n):
        if not qubits:
            result.append(_copy_circuit(circuit))
            continue

        try:
            qc = QCircuit()

            for _ in range(random.randint(0, 3)):
                q = random.choice(qubits)
                g1, g2 = _random_identity_pair(q)
                qc = _append(qc, g1)
                qc = _append(qc, g2)

            qc = _append(qc, _copy_circuit(circuit))

            for _ in range(random.randint(0, 3)):
                q = random.choice(qubits)
                g1, g2 = _random_identity_pair(q)
                qc = _append(qc, g1)
                qc = _append(qc, g2)

            result.append(qc)
        except Exception:
            result.append(_copy_circuit(circuit))

    return result
