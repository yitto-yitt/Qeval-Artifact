# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import *
import numbers


def remove_unassigned_parameterized_gates(circuit):
    def _is_numeric(x):
        return isinstance(x, numbers.Number) or isinstance(x, bool)

    def _is_unassigned_parameter(x):
        if _is_numeric(x) or x is None:
            return False

        if isinstance(x, str):
            try:
                float(x)
                return False
            except Exception:
                return True

        for name in ("is_bound", "bound", "is_assigned", "assigned"):
            if hasattr(x, name):
                try:
                    v = getattr(x, name)
                    v = v() if callable(v) else v
                    if isinstance(v, bool):
                        return not v
                except Exception:
                    pass

        for name in ("free_symbols", "parameters"):
            if hasattr(x, name):
                try:
                    v = getattr(x, name)
                    v = v() if callable(v) else v
                    if v:
                        return True
                except Exception:
                    pass

        for name in ("value", "val"):
            if hasattr(x, name):
                try:
                    v = getattr(x, name)
                    v = v() if callable(v) else v
                    if _is_numeric(v):
                        return False
                except Exception:
                    pass

        cls_name = type(x).__name__.lower()
        if "parameter" in cls_name or "symbol" in cls_name or cls_name in ("var", "variable"):
            return True

        try:
            float(x)
            return False
        except Exception:
            return False

    def _params(obj):
        for name in (
            "params",
            "parameters",
            "parameter",
            "get_params",
            "get_parameters",
            "get_parameter",
            "get_para",
            "get_angle",
            "angle",
        ):
            if hasattr(obj, name):
                try:
                    v = getattr(obj, name)
                    v = v() if callable(v) else v
                    if v is None:
                        continue
                    if isinstance(v, (list, tuple, set)):
                        return list(v)
                    return [v]
                except Exception:
                    pass
        return []

    def _has_unassigned_params(obj):
        return any(_is_unassigned_parameter(p) for p in _params(obj))

    def _items(obj):
        if hasattr(obj, "data"):
            try:
                return list(obj.data)
            except Exception:
                pass

        for name in (
            "get_instructions",
            "instructions",
            "get_nodes",
            "nodes",
            "get_node_list",
            "node_list",
            "get_gate_list",
            "gate_list",
            "gates",
        ):
            if hasattr(obj, name):
                try:
                    v = getattr(obj, name)
                    v = v() if callable(v) else v
                    return list(v)
                except Exception:
                    pass

        try:
            return list(obj)
        except Exception:
            pass

        return []

    def _op_qargs_cargs(item):
        if isinstance(item, tuple):
            if len(item) >= 3:
                return item[0], item[1], item[2]
            if len(item) == 2:
                return item[0], item[1], []
            if len(item) == 1:
                return item[0], [], []

        op = None
        for name in ("operation", "op", "gate", "instruction", "node"):
            if hasattr(item, name):
                try:
                    op = getattr(item, name)
                    op = op() if callable(op) else op
                    break
                except Exception:
                    pass
        if op is None:
            op = item

        qargs = []
        cargs = []
        for name in ("qubits", "qargs", "qbits"):
            if hasattr(item, name):
                try:
                    qargs = getattr(item, name)
                    qargs = qargs() if callable(qargs) else qargs
                    break
                except Exception:
                    pass
        for name in ("clbits", "cargs", "cbits"):
            if hasattr(item, name):
                try:
                    cargs = getattr(item, name)
                    cargs = cargs() if callable(cargs) else cargs
                    break
                except Exception:
                    pass

        return op, qargs, cargs

    def _new_like(obj):
        if hasattr(obj, "num_qubits") and hasattr(obj, "num_clbits"):
            try:
                return obj.__class__(obj.num_qubits, obj.num_clbits)
            except Exception:
                pass
        try:
            return obj.__class__()
        except Exception:
            try:
                return QCircuit()
            except Exception:
                return QProg()

    def _append(dst, op, qargs, cargs):
        try:
            dst.append(op, qargs, cargs)
            return dst
        except Exception:
            pass
        try:
            dst.append(op)
            return dst
        except Exception:
            pass
        try:
            dst.insert(op)
            return dst
        except Exception:
            pass
        try:
            dst << op
            return dst
        except Exception:
            pass
        return dst

    new_circuit = _new_like(circuit)

    for item in _items(circuit):
        op, qargs, cargs = _op_qargs_cargs(item)
        if not _has_unassigned_params(op):
            _append(new_circuit, op, qargs, cargs)

    return new_circuit
