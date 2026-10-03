# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import *
import numbers
import re


def remove_unassigned_parameterized_gates(circuit):
    def _is_number(x):
        if isinstance(x, numbers.Number):
            return True
        try:
            float(x)
            return True
        except Exception:
            return False

    def _as_sequence(x):
        if x is None:
            return []
        if isinstance(x, dict):
            return list(x.values())
        if isinstance(x, (list, tuple, set, frozenset)):
            return list(x)
        return [x]

    def _call_or_value(obj, name):
        if not hasattr(obj, name):
            return None, False
        val = getattr(obj, name)
        if callable(val):
            try:
                return val(), True
            except TypeError:
                return None, False
            except Exception:
                return None, False
        return val, True

    def _param_is_unassigned(p):
        if p is None:
            return False
        if isinstance(p, (list, tuple, set, frozenset, dict)):
            return any(_param_is_unassigned(v) for v in _as_sequence(p))
        if _is_number(p):
            return False
        if isinstance(p, str):
            return not _is_number(p)

        for attr in ("is_assigned", "assigned", "is_bound", "bound", "is_fixed"):
            val, ok = _call_or_value(p, attr)
            if ok and isinstance(val, bool):
                return not val

        for attr in ("value", "data", "val"):
            val, ok = _call_or_value(p, attr)
            if ok:
                if val is None:
                    return True
                if _is_number(val):
                    return False

        free, ok = _call_or_value(p, "parameters")
        if ok and free is not None:
            try:
                if len(free) > 0:
                    return True
            except Exception:
                pass

        name = type(p).__name__.lower()
        if any(k in name for k in ("parameter", "param", "var", "variable", "symbol", "expr", "expression")):
            return True

        return False

    def _gate_name(g):
        for attr in ("name", "gate_name", "get_name"):
            val, ok = _call_or_value(g, attr)
            if ok and val is not None:
                return str(val)
        for attr in ("gate_type", "get_gate_type", "type"):
            val, ok = _call_or_value(g, attr)
            if ok and val is not None:
                return str(val)
        return type(g).__name__

    def _looks_like_parameterized_gate(g):
        name = _gate_name(g).upper()
        keys = (
            "RX", "RY", "RZ", "RP", "U1", "U2", "U3", "U4", "U",
            "PHASE", "P", "CP", "CR", "CU", "RXX", "RYY", "RZZ", "RZX",
            "ISWAP", "TOFFOLI"
        )
        return any(name == k or name.startswith(k) for k in keys)

    def _string_suggests_unassigned_parameter(g):
        if not _looks_like_parameterized_gate(g):
            return False
        s = str(g)
        if any(x in s.lower() for x in ("parameter", "symbol", "var(")):
            return True
        s = re.sub(r"[qc]\s*\[\s*\d+\s*\]", " ", s, flags=re.IGNORECASE)
        s = re.sub(r"\b\d+(\.\d*)?([eE][+-]?\d+)?\b", " ", s)
        tokens = re.findall(r"[A-Za-z_]\w*", s)
        whitelist = {
            "qgate", "gate", "qubit", "qubits", "cbit", "cbits", "target", "targets",
            "control", "controls", "angle", "theta", "phi", "lambda", "pi", "e",
            "true", "false", "rx", "ry", "rz", "u1", "u2", "u3", "u4", "u",
            "phase", "p", "cp", "cr", "cu", "rxx", "ryy", "rzz", "rzx", "iswap",
            "toffoli", "q", "c"
        }
        gate_tokens = set(re.findall(r"[A-Za-z_]\w*", _gate_name(g).lower()))
        for t in tokens:
            tl = t.lower()
            if tl not in whitelist and tl not in gate_tokens:
                return True
        return False

    def _has_unassigned_parameters(g):
        found = False
        for attr in ("params", "parameters", "parameter", "get_params", "get_parameters", "get_parameter"):
            val, ok = _call_or_value(g, attr)
            if not ok:
                continue
            vals = _as_sequence(val)
            if vals:
                found = True
            if any(_param_is_unassigned(v) for v in vals):
                return True
        if found:
            return False
        return _string_suggests_unassigned_parameter(g)

    def _operation(item):
        if hasattr(item, "operation"):
            return item.operation
        if isinstance(item, (tuple, list)) and item:
            return item[0]
        for attr in ("get_gate", "get_qgate", "gate", "qgate"):
            val, ok = _call_or_value(item, attr)
            if ok and val is not None:
                return val
        return item

    def _empty_like(obj):
        try:
            return obj.__class__()
        except Exception:
            pass
        try:
            if "QProg" in type(obj).__name__:
                return QProg()
        except Exception:
            pass
        return QCircuit()

    def _append(dst, item):
        op = _operation(item)

        if hasattr(item, "operation") and hasattr(dst, "append"):
            try:
                r = dst.append(item.operation, item.qubits, item.clbits)
                return dst if r is None else r
            except Exception:
                pass

        if isinstance(item, (tuple, list)) and len(item) >= 3 and hasattr(dst, "append"):
            try:
                r = dst.append(item[0], item[1], item[2])
                return dst if r is None else r
            except Exception:
                pass

        for obj in (item, op):
            try:
                r = dst.__lshift__(obj)
                return dst if r is None else r
            except Exception:
                pass
            for meth in ("insert", "append"):
                if hasattr(dst, meth):
                    try:
                        r = getattr(dst, meth)(obj)
                        return dst if r is None else r
                    except Exception:
                        pass
        return dst

    def _items(obj):
        for attr in ("data", "instructions", "nodes", "gates"):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if callable(val):
                    try:
                        val = val()
                    except TypeError:
                        continue
                    except Exception:
                        continue
                try:
                    return list(val)
                except Exception:
                    pass
        for meth in ("get_instructions", "get_nodes", "get_gates", "get_qgates", "get_gate_list"):
            if hasattr(obj, meth):
                try:
                    return list(getattr(obj, meth)())
                except Exception:
                    pass
        try:
            return list(obj)
        except Exception:
            return None

    result = _empty_like(circuit)
    items = _items(circuit)

    if items is not None:
        for item in items:
            if not _has_unassigned_parameters(_operation(item)):
                result = _append(result, item)
        return result

    try:
        it = circuit.begin()
        end = circuit.end()
        while it != end:
            node = None
            for meth in ("get_node", "node"):
                if hasattr(it, meth):
                    try:
                        node = getattr(it, meth)()
                        break
                    except Exception:
                        pass
            if node is None:
                node = it
            if not _has_unassigned_parameters(_operation(node)):
                result = _append(result, node)
            moved = False
            for meth in ("get_next", "next", "__next__"):
                if hasattr(it, meth):
                    try:
                        it = getattr(it, meth)()
                        moved = True
                        break
                    except Exception:
                        pass
            if not moved:
                break
        return result
    except Exception:
        return result
