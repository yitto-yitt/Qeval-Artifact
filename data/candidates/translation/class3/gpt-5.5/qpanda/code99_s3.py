# EVAL_META: task_id=99, framework=qpanda, class=3
import re
import copy
from pyqpanda3.core import *

def remove_unassigned_parameterized_gates(circuit):
    def _is_number(x):
        if isinstance(x, bool):
            return True
        if isinstance(x, (int, float, complex)):
            return True
        try:
            float(x)
            return True
        except Exception:
            return False

    def _symbolic_string(s):
        s = str(s).strip()
        if not s:
            return False
        try:
            float(s)
            return False
        except Exception:
            pass
        t = re.sub(r'\b(pi|PI|Pi|e|E|sin|cos|tan|asin|acos|atan|sqrt|exp|log|ln|pow|abs)\b', '', s)
        return re.search(r'[A-Za-z_]\w*', t) is not None

    def _is_unassigned_param(p):
        if p is None or _is_number(p):
            return False
        if isinstance(p, str):
            return _symbolic_string(p)
        if isinstance(p, (list, tuple, set)):
            return any(_is_unassigned_param(x) for x in p)
        if isinstance(p, dict):
            return any(_is_unassigned_param(k) or _is_unassigned_param(v) for k, v in p.items())

        for name in ("is_bound", "bound", "is_assigned", "assigned", "is_initialized", "initialized"):
            if hasattr(p, name):
                try:
                    v = getattr(p, name)
                    v = v() if callable(v) else v
                    if v is False:
                        return True
                except Exception:
                    pass

        cls_name = p.__class__.__name__.lower()
        if any(k in cls_name for k in ("parameter", "variable", "var", "expr", "symbol")):
            return True

        return _symbolic_string(str(p))

    def _params_from(obj):
        params = []
        attr_names = (
            "params", "parameters", "parameter", "para", "angle", "angles",
            "theta", "phi", "lam", "lambda_", "gamma", "beta"
        )
        meth_names = (
            "get_params", "get_parameters", "get_parameter", "get_para",
            "get_angle", "get_angles", "get_theta", "get_phi", "get_lambda"
        )

        for name in attr_names:
            if hasattr(obj, name):
                try:
                    v = getattr(obj, name)
                    if not callable(v):
                        params.append(v)
                except Exception:
                    pass

        for name in meth_names:
            if hasattr(obj, name):
                try:
                    m = getattr(obj, name)
                    if callable(m):
                        params.append(m())
                except Exception:
                    pass

        return params

    def _operation_from_item(item):
        if hasattr(item, "operation"):
            return item.operation
        if isinstance(item, (tuple, list)) and item:
            return item[0]
        return item

    def _has_unassigned_parameters(item):
        op = _operation_from_item(item)
        params = _params_from(op)
        if not params:
            params = _params_from(item)
        return any(_is_unassigned_param(p) for p in params)

    def _append(dst, item):
        try:
            if hasattr(dst, "append"):
                op = _operation_from_item(item)
                if hasattr(item, "qubits") and hasattr(item, "clbits"):
                    dst.append(op, item.qubits, item.clbits)
                elif isinstance(item, (tuple, list)) and len(item) >= 3:
                    dst.append(item[0], item[1], item[2])
                else:
                    dst.append(item)
                return dst
        except Exception:
            pass

        try:
            if hasattr(dst, "insert"):
                dst.insert(item)
                return dst
        except Exception:
            pass

        try:
            return dst << item
        except Exception:
            pass

        return dst

    def _empty_like(obj):
        cls = obj.__class__
        try:
            return cls()
        except Exception:
            pass

        try:
            return QCircuit()
        except Exception:
            pass

        try:
            return QProg()
        except Exception:
            pass

        return copy.copy(obj)

    def _iter_items(obj):
        if hasattr(obj, "data"):
            try:
                return list(obj.data)
            except Exception:
                pass

        for name in ("instructions", "get_instructions", "nodes", "get_nodes", "get_node_list", "to_list"):
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
            return None

    def _originir(obj):
        for name in ("to_originir", "to_origin_ir", "toOriginIR", "originir", "origin_ir"):
            if hasattr(obj, name):
                try:
                    v = getattr(obj, name)
                    return v() if callable(v) else v
                except Exception:
                    pass

        for fn_name in ("convert_qprog_to_originir", "convert_qprog_to_origin_ir"):
            fn = globals().get(fn_name)
            if callable(fn):
                try:
                    return fn(obj)
                except Exception:
                    try:
                        machine = CPUQVM()
                        return fn(obj, machine)
                    except Exception:
                        pass
        return None

    def _line_has_unassigned_parameter(line):
        s = line.split("//", 1)[0].split("#", 1)[0].strip()
        if not s:
            return False

        upper = s.upper()
        if upper.startswith(("QINIT", "CREG", "MEASURE", "BARRIER", "DAGGER", "ENDDAGGER", "CONTROL", "ENDCONTROL")):
            return False

        parts = [p.strip() for p in s.split(",")]
        if len(parts) <= 1:
            return False

        for p in parts[1:]:
            if "q[" in p.lower() or "c[" in p.lower():
                continue
            p = p.strip("() ")
            if _symbolic_string(p):
                return True
        return False

    def _from_originir(text):
        for fn_name in ("convert_originir_to_qprog", "convert_origin_ir_to_qprog"):
            fn = globals().get(fn_name)
            if callable(fn):
                try:
                    return fn(text)
                except Exception:
                    try:
                        machine = CPUQVM()
                        return fn(text, machine)
                    except Exception:
                        pass
        return None

    items = _iter_items(circuit)
    if items is not None:
        new_circuit = _empty_like(circuit)
        for item in items:
            if not _has_unassigned_parameters(item):
                new_circuit = _append(new_circuit, item)
        return new_circuit

    ir = _originir(circuit)
    if isinstance(ir, str):
        filtered = "\n".join(line for line in ir.splitlines() if not _line_has_unassigned_parameter(line))
        rebuilt = _from_originir(filtered)
        if rebuilt is not None:
            return rebuilt

    return copy.deepcopy(circuit)
