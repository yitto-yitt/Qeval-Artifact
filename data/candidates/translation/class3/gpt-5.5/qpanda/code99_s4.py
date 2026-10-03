# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import *
import pyqpanda3.core as pq
import copy
import numbers


def remove_unassigned_parameterized_gates(circuit):
    def _is_numeric(x):
        if isinstance(x, numbers.Number):
            return True
        try:
            complex(x)
            return True
        except Exception:
            return False

    def _len_if_possible(x):
        try:
            return len(x)
        except Exception:
            try:
                return len(list(x))
            except Exception:
                return None

    def _call_noarg(obj, name):
        try:
            attr = getattr(obj, name)
        except Exception:
            return None, False
        if callable(attr):
            try:
                return attr(), True
            except TypeError:
                return None, False
            except Exception:
                return None, False
        return attr, True

    def _is_unassigned_parameter(p):
        if p is None:
            return False
        if _is_numeric(p):
            return False
        if isinstance(p, (str, bytes)):
            try:
                float(p)
                return False
            except Exception:
                return True

        for name in ("parameters", "free_symbols", "vars", "variables"):
            val, ok = _call_noarg(p, name)
            if ok:
                ln = _len_if_possible(val)
                if ln is not None and ln > 0:
                    return True
                if ln == 0:
                    continue

        for name in ("value", "val", "data", "get_value", "getValue", "eval", "evaluate"):
            val, ok = _call_noarg(p, name)
            if ok and val is not p and _is_numeric(val):
                return False

        try:
            float(p)
            return False
        except Exception:
            pass

        cls_name = p.__class__.__name__.lower()
        if (
            "parameter" in cls_name
            or "symbol" in cls_name
            or "expr" in cls_name
            or cls_name in ("var", "cvar")
            or "variable" in cls_name
        ):
            return True

        return True

    def _as_sequence(x):
        if x is None:
            return []
        if isinstance(x, (str, bytes)):
            return [x]
        if isinstance(x, dict):
            return list(x.values())
        if isinstance(x, (list, tuple, set, frozenset)):
            return list(x)
        try:
            return list(x)
        except Exception:
            return [x]

    def _params_of(obj):
        collected = []
        for name in (
            "params",
            "parameters",
            "parameter",
            "get_params",
            "get_param",
            "get_parameters",
            "get_parameter",
            "angles",
            "angle",
            "theta",
            "phi",
            "lam",
            "lambda",
            "gamma",
            "get_angles",
            "get_angle",
            "get_theta",
            "get_phi",
            "get_lambda",
        ):
            val, ok = _call_noarg(obj, name)
            if ok:
                collected.extend(_as_sequence(val))
        return collected

    def _has_unassigned_params(obj):
        params = _params_of(obj)
        if not params:
            return False
        return any(_is_unassigned_parameter(p) for p in params)

    def _new_container():
        cls = circuit.__class__
        if hasattr(circuit, "num_qubits"):
            try:
                nq = circuit.num_qubits() if callable(circuit.num_qubits) else circuit.num_qubits
                nc = getattr(circuit, "num_clbits", 0)
                nc = nc() if callable(nc) else nc
                return cls(nq, nc)
            except Exception:
                pass
        try:
            return cls()
        except Exception:
            pass

        name = cls.__name__.lower()
        if "prog" in name and hasattr(pq, "QProg"):
            return pq.QProg()
        if hasattr(pq, "QCircuit"):
            return pq.QCircuit()
        if hasattr(pq, "QProg"):
            return pq.QProg()
        return copy.copy(circuit)

    def _mapped_bits(original, result, bits, bit_attr, find_name):
        if bits is None:
            return None
        try:
            new_bits = getattr(result, bit_attr)
            old_find = getattr(original, find_name, None)
            mapped = []
            for b in bits:
                idx = None
                if old_find is not None:
                    try:
                        found = old_find(b)
                        idx = found.index if hasattr(found, "index") else found[0]
                    except Exception:
                        idx = None
                if idx is None:
                    try:
                        old_bits = getattr(original, bit_attr)
                        idx = list(old_bits).index(b)
                    except Exception:
                        idx = None
                mapped.append(new_bits[idx] if idx is not None else b)
            return mapped
        except Exception:
            return bits

    def _append_to(container, item, qargs=None, cargs=None):
        if qargs is not None:
            qargs2 = _mapped_bits(circuit, container, qargs, "qubits", "find_bit")
            cargs2 = _mapped_bits(circuit, container, cargs, "clbits", "find_bit") if cargs is not None else []
            try:
                container.append(item, qargs2, cargs2)
                return container
            except Exception:
                pass
            try:
                container.append(item, qargs2)
                return container
            except Exception:
                pass

        for method in ("insert", "append", "push_back"):
            try:
                m = getattr(container, method)
            except Exception:
                continue
            try:
                r = m(item)
                return r if r is not None else container
            except Exception:
                pass

        try:
            r = container << item
            return r if r is not None else container
        except Exception:
            pass

        return container

    result = _new_container()

    if hasattr(circuit, "data"):
        try:
            data = list(circuit.data.copy())
        except Exception:
            try:
                data = list(circuit.data)
            except Exception:
                data = []
        for instruction in data:
            if hasattr(instruction, "operation"):
                instr = instruction.operation
                qargs = getattr(instruction, "qubits", [])
                cargs = getattr(instruction, "clbits", [])
            elif isinstance(instruction, (tuple, list)) and len(instruction) >= 1:
                instr = instruction[0]
                qargs = instruction[1] if len(instruction) > 1 else []
                cargs = instruction[2] if len(instruction) > 2 else []
            else:
                instr = instruction
                qargs = []
                cargs = []
            if not _has_unassigned_params(instr):
                result = _append_to(result, instr, qargs, cargs)
        return result

    items = None
    for name in (
        "get_gate_list",
        "get_gates",
        "get_qgate_list",
        "get_instruction_list",
        "get_instructions",
        "get_nodes",
        "nodes",
        "instructions",
        "gates",
    ):
        val, ok = _call_noarg(circuit, name)
        if ok:
            try:
                items = list(val)
                break
            except Exception:
                pass

    if items is None:
        try:
            items = list(circuit)
        except Exception:
            return copy.deepcopy(circuit)

    for item in items:
        op = getattr(item, "operation", item)
        if not _has_unassigned_params(op):
            result = _append_to(result, item)

    return result
