# EVAL_META: task_id=109, framework=qpanda, class=3
import pyqpanda3.core as pq

def circuit():
    last_error = None

    def parameter_candidates():
        candidates = []
        for name in ("Parameter", "QParameter", "Var"):
            obj = getattr(pq, name, None)
            if obj is not None:
                for args in (("th",), (0.0,)):
                    try:
                        candidates.append(obj(*args))
                        break
                    except Exception:
                        pass
        for name in ("parameter", "create_parameter", "var"):
            obj = getattr(pq, name, None)
            if obj is not None:
                for args in (("th",), (0.0,)):
                    try:
                        candidates.append(obj(*args))
                        break
                    except Exception:
                        pass
        candidates.append(0.0)
        return candidates

    def add(container, op):
        if hasattr(container, "insert"):
            r = container.insert(op)
            return container if r is None else r
        r = container.__lshift__(op)
        return container if r is None else r

    def build_gate_circuit(wire, theta, circuit_args):
        qc = pq.QCircuit(*circuit_args)
        h_gate = getattr(pq, "H")
        rz_gate = getattr(pq, "RZ")
        qc = add(qc, h_gate(wire))
        try:
            rz = rz_gate(wire, theta)
        except Exception:
            rz = rz_gate(theta, wire)
        qc = add(qc, rz)
        return qc

    for theta in parameter_candidates():
        for circuit_args in ((), (1,)):
            try:
                return build_gate_circuit(0, theta, circuit_args)
            except Exception as exc:
                last_error = exc

    for theta in parameter_candidates():
        for circuit_args in ((), (1,)):
            try:
                qc = pq.QCircuit(*circuit_args)
                h_method = getattr(qc, "h", None) or getattr(qc, "H", None)
                rz_method = getattr(qc, "rz", None) or getattr(qc, "RZ", None)
                r = h_method(0)
                if r is not None:
                    qc = r
                try:
                    r = rz_method(0, theta)
                except Exception:
                    r = rz_method(theta, 0)
                if r is not None:
                    qc = r
                return qc
            except Exception as exc:
                last_error = exc

    qvm_cls = getattr(pq, "CPUQVM", None)
    if qvm_cls is not None:
        for theta in parameter_candidates():
            try:
                qvm = qvm_cls()
                for init_name in ("init_qvm", "init", "initQVM"):
                    init = getattr(qvm, init_name, None)
                    if init is not None:
                        init()
                        break
                alloc = getattr(qvm, "qAlloc_many", None) or getattr(qvm, "qalloc_many", None)
                q = alloc(1)
                circuit._qvm = qvm
                return build_gate_circuit(q[0], theta, ())
            except Exception as exc:
                last_error = exc

    raise last_error if last_error is not None else RuntimeError("Unable to construct pyQPanda3 circuit")
