# EVAL_META: task_id=99, framework=qpanda2, class=3
import ast
import math
import re
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
try:
    qubits = machine.qAlloc_many(0)
except Exception:
    qubits = []

atexit.register(machine.finalize)

def remove_unassigned_parameterized_gates(circuit):
    def _is_unassigned_object(obj):
        cls_name = obj.__class__.__name__
        if cls_name in ("Parameter", "ParameterVectorElement"):
            return True
        params = getattr(obj, "parameters", None)
        try:
            return bool(params)
        except Exception:
            return False

    if hasattr(circuit, "data") and hasattr(circuit, "num_qubits"):
        try:
            new_circuit = circuit.__class__(circuit.num_qubits, getattr(circuit, "num_clbits", 0))
            for instruction in list(circuit.data):
                instr = getattr(instruction, "operation", instruction[0])
                qargs = getattr(instruction, "qubits", instruction[1])
                cargs = getattr(instruction, "clbits", instruction[2])
                params = list(getattr(instr, "params", []))
                if params and _is_unassigned_object(params[0]):
                    continue
                qidx = [circuit.find_bit(qb).index for qb in qargs]
                cidx = [circuit.find_bit(cb).index for cb in cargs]
                new_circuit.append(instr, qidx, cidx)
            return new_circuit
        except Exception:
            pass

    def _convert_to_originir(obj):
        if isinstance(obj, str):
            return obj
        names = ("convert_qprog_to_originir", "transform_qprog_to_originir")
        candidates = [obj]
        try:
            wrapped = pq.QProg()
            wrapped.insert(obj)
            candidates.append(wrapped)
        except Exception:
            pass
        last_error = None
        for candidate in candidates:
            for name in names:
                fn = getattr(pq, name, None)
                if fn is None:
                    continue
                for args in ((candidate, machine), (candidate,)):
                    try:
                        ir = fn(*args)
                        if isinstance(ir, bytes):
                            ir = ir.decode()
                        if isinstance(ir, str):
                            return ir
                    except Exception as exc:
                        last_error = exc
        if last_error is not None:
            raise last_error
        raise RuntimeError("Unable to convert circuit to OriginIR")

    def _split_top_level_commas(text):
        parts = []
        start = 0
        depth = 0
        for i, ch in enumerate(text):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == "," and depth == 0:
                parts.append(text[start:i].strip())
                start = i + 1
        parts.append(text[start:].strip())
        return parts

    def _parenthesized_groups(text):
        groups = []
        start = None
        depth = 0
        for i, ch in enumerate(text):
            if ch == "(":
                if depth == 0:
                    start = i + 1
                depth += 1
            elif ch == ")":
                if depth:
                    depth -= 1
                    if depth == 0 and start is not None:
                        groups.append(text[start:i])
                        start = None
        return groups

    def _expr_is_assigned(expr):
        expr = expr.strip()
        if not expr:
            return True
        try:
            float(expr)
            return True
        except Exception:
            pass
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        allowed.update({"pi": math.pi, "PI": math.pi, "e": math.e, "E": math.e, "tau": math.tau, "math": math})
        try:
            tree = ast.parse(expr, mode="eval")
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and node.id not in allowed:
                    return False
                if isinstance(node, (ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.Assign, ast.AugAssign)):
                    return False
            eval(compile(tree, "<originir-param>", "eval"), {"__builtins__": {}}, allowed)
            return True
        except Exception:
            return False

    def _line_has_unassigned_parameter(line):
        stripped = line.strip()
        if not stripped:
            return False
        upper = stripped.split()[0].upper() if stripped.split() else ""
        if upper in {"QINIT", "CREG", "MEASURE", "BARRIER", "RESET", "DAGGER", "ENDDAGGER", "CONTROL", "ENDCONTROL"}:
            return False
        groups = _parenthesized_groups(stripped)
        if not groups:
            return False
        for group in groups:
            for expr in _split_top_level_commas(group):
                if expr and not _expr_is_assigned(expr):
                    return True
        return False

    def _filter_originir(originir):
        filtered = []
        for line in originir.splitlines():
            if not _line_has_unassigned_parameter(line):
                filtered.append(line)
        return "\n".join(filtered) + ("\n" if filtered else "")

    def _convert_from_originir(originir):
        names = (
            "convert_originir_string_to_qprog",
            "convert_originir_to_qprog",
            "transform_originir_to_qprog",
        )
        last_error = None
        for name in names:
            fn = getattr(pq, name, None)
            if fn is None:
                continue
            for args in ((originir, machine), (originir,)):
                try:
                    result = fn(*args)
                    if isinstance(result, (tuple, list)) and result:
                        return result[0]
                    return result
                except Exception as exc:
                    last_error = exc
        if last_error is not None:
            raise last_error
        raise RuntimeError("Unable to convert OriginIR to QProg")

    originir = _convert_to_originir(circuit)
    filtered_originir = _filter_originir(originir)
    return _convert_from_originir(filtered_originir)
