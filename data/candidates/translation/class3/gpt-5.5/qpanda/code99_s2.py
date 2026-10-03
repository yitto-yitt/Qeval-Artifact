# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import *


def remove_unassigned_parameterized_gates(circuit):
    def _call_noarg(obj, name):
        try:
            attr = getattr(obj, name)
        except Exception:
            return None, False
        try:
            if callable(attr):
                return attr(), True
            return attr, True
        except Exception:
            return None, False

    def _is_numeric(value):
        if value is None:
            return True
        if isinstance(value, (int, float, complex, bool)):
            return True
        try:
            float(value)
            return True
        except Exception:
            return False

    def _is_symbolic_parameter(value):
        if value is None:
            return False
        if isinstance(value, (list, tuple)):
            return any(_is_symbolic_parameter(v) for v in value)
        if _is_numeric(value):
            return False
        cls_name = value.__class__.__name__.lower()
        mod_name = getattr(value.__class__, "__module__", "").lower()
        if (
            "parameter" in cls_name
            or "param" in cls_name
            or "expression" in cls_name
            or "expr" in cls_name
            or cls_name in ("var", "variable")
            or "symbol" in cls_name
        ):
            return True
        if "pyqpanda" in mod_name and not _is_numeric(value):
            return True
        text = str(value)
        if "Parameter" in text or "param" in text.lower() or "{" in text or "}" in text:
            return True
        return False

    def _extract_params(obj):
        if obj is None:
            return []
        for name in (
            "params",
            "parameters",
            "parameter",
            "angles",
            "angle",
            "theta",
            "phi",
            "lambda_",
            "gamma",
            "beta",
            "get_params",
            "get_parameters",
            "get_parameter",
            "get_angles",
            "get_angle",
        ):
            value, ok = _call_noarg(obj, name)
            if ok:
                if value is None:
                    continue
                if isinstance(value, (list, tuple)):
                    return list(value)
                return [value]
        return []

    def _has_unassigned_parameter(obj):
        params = _extract_params(obj)
        if not params:
            return False
        return _is_symbolic_parameter(params[0])

    def _operation_from_item(item):
        if hasattr(item, "operation"):
            try:
                return item.operation
            except Exception:
                pass
        if hasattr(item, "gate"):
            try:
                return item.gate
            except Exception:
                pass
        if isinstance(item, (tuple, list)) and item:
            return item[0]
        return item

    def _qargs_cargs_from_item(item):
        if hasattr(item, "qubits") or hasattr(item, "clbits"):
            try:
                return getattr(item, "qubits", []), getattr(item, "clbits", [])
            except Exception:
                return None, None
        if isinstance(item, (tuple, list)) and len(item) >= 3:
            return item[1], item[2]
        return None, None

    def _iter_items(obj):
        if hasattr(obj, "data"):
            try:
                return list(obj.data)
            except Exception:
                pass
        for name in ("instructions", "operations", "ops", "nodes", "get_nodes"):
            value, ok = _call_noarg(obj, name)
            if ok and value is not None:
                try:
                    return list(value)
                except Exception:
                    pass
        try:
            return list(obj)
        except Exception:
            pass

        items = []
        try:
            it = obj.begin()
            end = obj.end()
            guard = 0
            while it != end and guard < 100000:
                guard += 1
                try:
                    node = it.get_node()
                except Exception:
                    node = it
                items.append(node)
                try:
                    it = it.get_next()
                except Exception:
                    try:
                        it = next(it)
                    except Exception:
                        break
            return items
        except Exception:
            return []

    def _new_circuit_like(obj):
        try:
            return type(obj)()
        except Exception:
            return QCircuit()

    def _append_to(container, item, op, qargs, cargs):
        if qargs is not None:
            for name in ("append", "insert"):
                try:
                    method = getattr(container, name)
                    method(op, qargs, cargs)
                    return container
                except Exception:
                    pass

        for element in (item, op):
            if element is None:
                continue
            try:
                result = container.__lshift__(element)
                if result is not None and hasattr(result, "__lshift__"):
                    return result
                return container
            except Exception:
                pass
            try:
                result = container.insert(element)
                if result is not None and hasattr(result, "__lshift__"):
                    return result
                return container
            except Exception:
                pass
            try:
                result = container.append(element)
                if result is not None and hasattr(result, "__lshift__"):
                    return result
                return container
            except Exception:
                pass
        return container

    circuit_without_params = _new_circuit_like(circuit)

    for item in _iter_items(circuit):
        op = _operation_from_item(item)
        qargs, cargs = _qargs_cargs_from_item(item)
        if not (_has_unassigned_parameter(op) or _has_unassigned_parameter(item)):
            circuit_without_params = _append_to(circuit_without_params, item, op, qargs, cargs)

    return circuit_without_params
