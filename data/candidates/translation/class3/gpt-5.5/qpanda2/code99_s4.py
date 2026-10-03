# EVAL_META: task_id=99, framework=qpanda2, class=3
import re
import math
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(32)
c = machine.cAlloc_many(32)


def remove_unassigned_parameterized_gates(circuit):
    def _is_numeric_value(x):
        if isinstance(x, (int, float, complex)):
            return True
        try:
            float(x)
            return True
        except Exception:
            return False

    def _is_unassigned_param(x):
        if x is None:
            return False
        params = getattr(x, "parameters", None)
        try:
            if params:
                return True
        except Exception:
            pass
        return not _is_numeric_value(x)

    if hasattr(circuit, "data") and hasattr(circuit, "copy_empty_like"):
        new_circuit = circuit.copy_empty_like()
        for instruction in list(circuit.data):
            instr = getattr(instruction, "operation", instruction[0])
            qargs = getattr(instruction, "qubits", instruction[1])
            cargs = getattr(instruction, "clbits", instruction[2])
            params = getattr(instr, "params", [])
            remove_gate = False
            if isinstance(params, (list, tuple)):
                remove_gate = any(_is_unassigned_param(p) for p in params)
            else:
                remove_gate = _is_unassigned_param(params)
            if not remove_gate:
                new_circuit.append(instr, qargs, cargs)
        return new_circuit

    def _safe_eval_expr(expr):
        expr = expr.strip()
        while expr.startswith("(") and expr.endswith(")"):
            depth = 0
            valid = True
            for i, ch in enumerate(expr):
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0 and i != len(expr) - 1:
                        valid = False
                        break
            if valid:
                expr = expr[1:-1].strip()
            else:
                break
        env = {
            "pi": math.pi,
            "PI": math.pi,
            "e": math.e,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sqrt": math.sqrt,
            "exp": math.exp,
            "log": math.log,
        }
        try:
            return float(eval(expr, {"__builtins__": {}}, env))
        except Exception:
            raise ValueError(expr)

    def _line_has_unassigned_parameter(line):
        if not re.search(r"\([^()]*\)", line):
            return False
        for expr in re.findall(r"\(([^()]*)\)", line):
            try:
                _safe_eval_expr(expr)
            except Exception:
                return True
        return False

    prog = pq.QProg()
    try:
        prog << circuit
    except Exception:
        prog = circuit

    try:
        originir = pq.convert_qprog_to_originir(prog, machine)
        filtered_lines = []
        for line in originir.splitlines():
            stripped = line.strip()
            if not stripped or not _line_has_unassigned_parameter(stripped):
                filtered_lines.append(line)
        filtered_originir = "\n".join(filtered_lines)

        parser = getattr(pq, "convert_originir_string_to_qprog", None)
        if parser is None:
            parser = getattr(pq, "convert_originir_to_qprog", None)
        if parser is not None:
            parsed = parser(filtered_originir, machine)
            if isinstance(parsed, tuple):
                return parsed[0]
            return parsed
    except Exception:
        pass

    originir = pq.convert_qprog_to_originir(prog, machine)
    result = pq.QProg()
    controls = []
    dagger_depth = 0

    for raw_line in originir.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("QINIT") or line.startswith("CREG"):
            continue
        upper = line.upper()
        if upper.startswith("CONTROL"):
            idxs = [int(x) for x in re.findall(r"q\[(\d+)\]", line)]
            controls.extend(q[i] for i in idxs if i < len(q))
            continue
        if upper.startswith("ENDCONTROL"):
            if controls:
                controls.pop()
            continue
        if upper == "DAGGER":
            dagger_depth += 1
            continue
        if upper == "ENDDAGGER":
            dagger_depth = max(0, dagger_depth - 1)
            continue
        if _line_has_unassigned_parameter(line):
            continue

        name = upper.split()[0]
        qidx = [int(x) for x in re.findall(r"q\[(\d+)\]", line)]
        cidx = [int(x) for x in re.findall(r"c\[(\d+)\]", line)]
        params = [_safe_eval_expr(x) for x in re.findall(r"\(([^()]*)\)", line)]

        gate = None
        if name == "MEASURE" and qidx and cidx:
            result << pq.Measure(q[qidx[0]], c[cidx[0]])
            continue
        if name == "H" and qidx:
            gate = pq.H(q[qidx[0]])
        elif name == "X" and qidx:
            gate = pq.X(q[qidx[0]])
        elif name == "Y" and qidx:
            gate = pq.Y(q[qidx[0]])
        elif name == "Z" and qidx:
            gate = pq.Z(q[qidx[0]])
        elif name == "S" and qidx:
            gate = pq.S(q[qidx[0]])
        elif name == "T" and qidx:
            gate = pq.T(q[qidx[0]])
        elif name == "X1" and qidx:
            gate = pq.X1(q[qidx[0]])
        elif name == "Y1" and qidx:
            gate = pq.Y1(q[qidx[0]])
        elif name == "Z1" and qidx:
            gate = pq.Z1(q[qidx[0]])
        elif name in ("I", "ID") and qidx:
            gate = pq.I(q[qidx[0]])
        elif name in ("CNOT", "CX") and len(qidx) >= 2:
            gate = pq.CNOT(q[qidx[0]], q[qidx[1]])
        elif name == "CZ" and len(qidx) >= 2:
            gate = pq.CZ(q[qidx[0]], q[qidx[1]])
        elif name == "SWAP" and len(qidx) >= 2:
            gate = pq.SWAP(q[qidx[0]], q[qidx[1]])
        elif name == "ISWAP" and len(qidx) >= 2:
            gate = pq.iSWAP(q[qidx[0]], q[qidx[1]])
        elif name == "SQISWAP" and len(qidx) >= 2:
            gate = pq.SqiSWAP(q[qidx[0]], q[qidx[1]])
        elif name == "RX" and qidx and len(params) >= 1:
            gate = pq.RX(q[qidx[0]], params[0])
        elif name == "RY" and qidx and len(params) >= 1:
            gate = pq.RY(q[qidx[0]], params[0])
        elif name == "RZ" and qidx and len(params) >= 1:
            gate = pq.RZ(q[qidx[0]], params[0])
        elif name == "U1" and qidx and len(params) >= 1:
            gate = pq.U1(q[qidx[0]], params[0])
        elif name == "U2" and qidx and len(params) >= 2:
            gate = pq.U2(q[qidx[0]], params[0], params[1])
        elif name == "U3" and qidx and len(params) >= 3:
            gate = pq.U3(q[qidx[0]], params[0], params[1], params[2])
        elif name == "U4" and qidx and len(params) >= 4:
            gate = pq.U4(q[qidx[0]], params[0], params[1], params[2], params[3])

        if gate is not None:
            if dagger_depth % 2 == 1:
                gate = gate.dagger()
            if controls:
                gate = gate.control(controls)
            result << gate

    return result


atexit.register(machine.finalize)
