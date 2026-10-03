# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq


def rx_gate(value=None):
    def _append_gate(circuit, gate):
        try:
            result = circuit << gate
            return circuit if result is None else result
        except Exception:
            result = circuit.insert(gate)
            return circuit if result is None else result

    def _parameter_candidates():
        if value is not None:
            return [value]
        candidates = []
        for name in ("Parameter", "QParameter", "ParameterExpression", "Var", "Variable"):
            cls = getattr(pq, name, None)
            if cls is not None:
                try:
                    candidates.append(cls("theta"))
                except Exception:
                    pass
        candidates.append("theta")
        return candidates

    def _allocated_qubit():
        qvm_cls = getattr(pq, "CPUQVM", None)
        if qvm_cls is None:
            return None, None
        qvm = qvm_cls()
        for init_name in ("init_qvm", "init", "initialize"):
            init = getattr(qvm, init_name, None)
            if init is not None:
                try:
                    init()
                except Exception:
                    pass
                break
        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            alloc = getattr(qvm, alloc_name, None)
            if alloc is not None:
                try:
                    qv = alloc(1)
                    return qvm, qv[0]
                except Exception:
                    pass
        for alloc_name in ("qAlloc", "qalloc", "allocate_qubit"):
            alloc = getattr(qvm, alloc_name, None)
            if alloc is not None:
                try:
                    return qvm, alloc()
                except Exception:
                    pass
        return qvm, None

    last_error = None
    for q in (0,):
        for angle in _parameter_candidates():
            try:
                circuit = pq.QCircuit()
                return _append_gate(circuit, pq.RX(q, angle))
            except Exception as exc:
                last_error = exc

    qvm, q = _allocated_qubit()
    if q is not None:
        for angle in _parameter_candidates():
            try:
                circuit = pq.QCircuit()
                circuit = _append_gate(circuit, pq.RX(q, angle))
                try:
                    circuit._qvm = qvm
                except Exception:
                    pass
                return circuit
            except Exception as exc:
                last_error = exc

    raise last_error if last_error is not None else RuntimeError("Unable to construct RX circuit")
