# EVAL_META: task_id=24, framework=pennylane, class=1
import inspect
import numpy as np
import pennylane as qml

def dj_algorithm(oracle):
    def _as_int(value):
        try:
            return int(value)
        except Exception:
            return None

    def _wire_list(obj):
        if hasattr(obj, "wires"):
            try:
                ws = list(obj.wires)
                if len(ws) > 0:
                    return ws
            except Exception:
                pass
        if hasattr(obj, "num_qubits"):
            n_val = _as_int(obj.num_qubits)
            if n_val is not None:
                return list(range(n_val))
        if hasattr(obj, "num_wires"):
            n_val = _as_int(obj.num_wires)
            if n_val is not None:
                return list(range(n_val))
        raise ValueError("Cannot determine the number of oracle qubits/wires.")

    wires = _wire_list(oracle)
    n = len(wires)
    input_wires = wires[:-1]

    def _apply_qiskit_circuit(circ):
        qubits = list(circ.qubits)

        def qindex(q):
            try:
                return circ.find_bit(q).index
            except Exception:
                return qubits.index(q)

        for item in circ.data:
            if hasattr(item, "operation"):
                op = item.operation
                qargs = list(item.qubits)
            else:
                op = item[0]
                qargs = list(item[1])

            name = getattr(op, "name", "").lower()
            if name in {"barrier", "measure", "delay"}:
                continue

            qw = [wires[qindex(q)] for q in qargs]
            params = [float(p) for p in getattr(op, "params", [])]

            if name in {"id", "iden", "i"}:
                continue
            elif name == "x":
                qml.PauliX(wires=qw[0])
            elif name == "y":
                qml.PauliY(wires=qw[0])
            elif name == "z":
                qml.PauliZ(wires=qw[0])
            elif name == "h":
                qml.Hadamard(wires=qw[0])
            elif name == "s":
                qml.S(wires=qw[0])
            elif name == "sdg":
                qml.adjoint(qml.S)(wires=qw[0])
            elif name == "t":
                qml.T(wires=qw[0])
            elif name == "tdg":
                qml.adjoint(qml.T)(wires=qw[0])
            elif name == "rx":
                qml.RX(params[0], wires=qw[0])
            elif name == "ry":
                qml.RY(params[0], wires=qw[0])
            elif name == "rz":
                qml.RZ(params[0], wires=qw[0])
            elif name in {"p", "phase", "u1"}:
                qml.PhaseShift(params[0], wires=qw[0])
            elif name in {"u", "u3"}:
                qml.U3(params[0], params[1], params[2], wires=qw[0])
            elif name in {"cx", "cnot"}:
                qml.CNOT(wires=qw)
            elif name == "cy":
                qml.CY(wires=qw)
            elif name == "cz":
                qml.CZ(wires=qw)
            elif name in {"cp", "cu1"}:
                qml.ControlledPhaseShift(params[0], wires=qw)
            elif name == "swap":
                qml.SWAP(wires=qw)
            elif name == "cswap":
                qml.CSWAP(wires=qw)
            elif name == "ccx":
                qml.Toffoli(wires=qw)
            elif name in {"mcx", "mct"}:
                qml.MultiControlledX(wires=qw)
            else:
                matrix = np.asarray(op.to_matrix(), dtype=complex)
                qml.QubitUnitary(matrix, wires=qw)

    def _apply_object(obj):
        if isinstance(obj, qml.operation.Operator):
            qml.apply(obj)
            return True
        if isinstance(obj, (list, tuple)):
            for sub in obj:
                _apply_object(sub)
            return True
        if hasattr(obj, "operations"):
            for sub in obj.operations:
                _apply_object(sub)
            return True
        if hasattr(obj, "data") and hasattr(obj, "qubits"):
            _apply_qiskit_circuit(obj)
            return True
        return False

    def _apply_oracle():
        if _apply_object(oracle):
            return

        if callable(oracle):
            try:
                sig = inspect.signature(oracle)
                params = list(sig.parameters.values())
                has_var_kw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params)
                has_var_pos = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params)
                has_wires = any(
                    p.name == "wires"
                    and p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
                    for p in params
                )
                positional = [
                    p for p in params
                    if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
                    and p.default is inspect.Parameter.empty
                ]

                if has_wires or has_var_kw:
                    oracle(wires=wires)
                elif len(positional) >= 1 or has_var_pos:
                    oracle(wires)
                else:
                    oracle()
                return
            except (ValueError, TypeError):
                pass

            try:
                oracle(wires=wires)
                return
            except TypeError:
                try:
                    oracle(wires)
                    return
                except TypeError:
                    oracle()
                    return

        raise TypeError("Unsupported oracle type.")

    dev = qml.device("default.qubit", wires=wires)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=wires[-1])
        for w in wires:
            qml.Hadamard(wires=w)
        _apply_oracle()
        for w in wires:
            qml.Hadamard(wires=w)
        return qml.probs(wires=input_wires)

    probs = np.asarray(circuit(), dtype=float)
    m = n - 1
    distribution = {}

    for idx, prob in enumerate(probs):
        if prob > 1e-12:
            bits = format(idx, f"0{m}b")
            distribution[bits[::-1]] = float(prob)

    return distribution
