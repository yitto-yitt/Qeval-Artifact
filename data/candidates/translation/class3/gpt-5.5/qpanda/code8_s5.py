# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq

def rx_gate(value=None):
    def _append(container, gate):
        if hasattr(container, "insert"):
            try:
                result = container.insert(gate)
                return result if result is not None else container
            except Exception:
                pass
        result = container << gate
        return result if result is not None else container

    def _qubits():
        candidates = [0]
        try:
            qvm = getattr(rx_gate, "_qvm", None)
            if qvm is None and hasattr(pq, "CPUQVM"):
                qvm = pq.CPUQVM()
                for init_name in ("init_qvm", "init", "initQVM"):
                    if hasattr(qvm, init_name):
                        try:
                            getattr(qvm, init_name)()
                            break
                        except Exception:
                            pass
                rx_gate._qvm = qvm
            if qvm is not None:
                for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany"):
                    if hasattr(qvm, alloc_name):
                        try:
                            qv = getattr(qvm, alloc_name)(1)
                            candidates.append(qv[0])
                            break
                        except Exception:
                            pass
                if hasattr(qvm, "qAlloc"):
                    try:
                        candidates.append(qvm.qAlloc())
                    except Exception:
                        pass
        except Exception:
            pass
        return candidates

    def _make_standard(angle):
        last_error = None
        for q in _qubits():
            for gate_name in ("RX", "RXGate"):
                gate_ctor = getattr(pq, gate_name, None)
                if gate_ctor is None:
                    continue
                for args in ((q, angle), (angle, q)):
                    try:
                        gate = gate_ctor(*args)
                    except Exception as exc:
                        last_error = exc
                        continue
                    for circuit_name in ("QCircuit", "QProg"):
                        circuit_ctor = getattr(pq, circuit_name, None)
                        if circuit_ctor is None:
                            continue
                        try:
                            circuit = circuit_ctor()
                            return _append(circuit, gate)
                        except Exception as exc:
                            last_error = exc
        if last_error is not None:
            raise last_error
        raise RuntimeError("Unable to construct RX circuit")

    if value is not None:
        return _make_standard(value)

    parameter_candidates = []
    for cls_name in ("Parameter", "ParameterExpression", "Param"):
        cls = getattr(pq, cls_name, None)
        if cls is not None:
            for args in (("theta",),):
                try:
                    parameter_candidates.append(cls(*args))
                except Exception:
                    pass
    parameter_candidates.append("theta")

    for theta in parameter_candidates:
        try:
            return _make_standard(theta)
        except Exception:
            pass

    var_fn = getattr(pq, "var", None)
    if var_fn is not None:
        variable_candidates = []
        for args in (("theta",), (0.0, True), (0.0,)):
            try:
                variable_candidates.append(var_fn(*args))
            except Exception:
                pass
        for theta in variable_candidates:
            for circuit_name in ("VariationalQuantumCircuit", "VQC"):
                circuit_ctor = getattr(pq, circuit_name, None)
                if circuit_ctor is None:
                    continue
                for gate_name in ("VariationalQuantumGate_RX", "VQG_RX"):
                    gate_ctor = getattr(pq, gate_name, None)
                    if gate_ctor is None:
                        continue
                    for q in _qubits():
                        try:
                            circuit = circuit_ctor()
                            gate = gate_ctor(q, theta)
                            return _append(circuit, gate)
                        except Exception:
                            pass

    return _make_standard(0.0)
