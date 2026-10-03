# EVAL_META: task_id=7, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_parametrized_gate():
    def _get_machine():
        if hasattr(create_parametrized_gate, "_machine"):
            return create_parametrized_gate._machine
        last_error = None
        for name in ("CPUQVM", "CPUSingleThreadQVM", "QVM", "QuantumMachine"):
            cls = getattr(pq, name, None)
            if cls is None:
                continue
            try:
                machine = cls()
                for init_name in ("init", "init_qvm", "initialize"):
                    init = getattr(machine, init_name, None)
                    if init is not None:
                        try:
                            init()
                        except TypeError:
                            pass
                        break
                create_parametrized_gate._machine = machine
                return machine
            except Exception as exc:
                last_error = exc
        if last_error is not None:
            raise last_error
        return None

    def _alloc_qubit(machine):
        if machine is not None:
            for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
                method = getattr(machine, name, None)
                if method is None:
                    continue
                try:
                    qubits = method(1)
                    return qubits[0]
                except Exception:
                    pass
            for name in ("qAlloc", "qalloc", "allocate_qubit"):
                method = getattr(machine, name, None)
                if method is None:
                    continue
                try:
                    return method()
                except Exception:
                    try:
                        return method(0)
                    except Exception:
                        pass
        return 0

    def _new_circuit():
        cls = getattr(pq, "QCircuit")
        try:
            return cls()
        except Exception:
            return cls(1)

    def _append(container, gate):
        try:
            result = container << gate
            return container if result is None else result
        except Exception:
            pass
        for name in ("insert", "append", "add_gate", "push_back"):
            method = getattr(container, name, None)
            if method is None:
                continue
            try:
                result = method(gate)
                return container if result is None else result
            except Exception:
                pass
        raise TypeError("Unable to append gate to circuit")

    def _parameter_candidates():
        seen = set()

        def emit(value):
            key = (type(value), repr(value))
            if key in seen:
                return None
            seen.add(key)
            return value

        value = emit("theta")
        if value is not None:
            yield value

        names = [
            "Parameter",
            "QParameter",
            "QParam",
            "QGateParam",
            "ParameterExpression",
            "QParameterExpression",
            "Expression",
            "Expr",
            "QExpr",
        ]
        names.extend(
            n for n in dir(pq)
            if ("param" in n.lower() or "expr" in n.lower())
            and n not in names
        )

        argument_lists = [
            ("theta",),
            ("theta", 0.0),
            ("theta", True),
            ("theta", 0.0, True),
            (0.0, "theta"),
            (0.0, True, "theta"),
        ]

        for name in names:
            ctor = getattr(pq, name, None)
            if ctor is None or not callable(ctor):
                continue
            for args in argument_lists:
                try:
                    value = emit(ctor(*args))
                    if value is not None:
                        yield value
                except Exception:
                    pass

        for name in ("var", "Var"):
            ctor = getattr(pq, name, None)
            if ctor is None or not callable(ctor):
                continue
            for args in ((0.0, True), (0.0,), ([0.0], True), ([0.0],)):
                try:
                    value = emit(ctor(*args))
                    if value is not None:
                        yield value
                except Exception:
                    pass

    machine = _get_machine()
    q = _alloc_qubit(machine)
    last_error = None

    for theta in _parameter_candidates():
        try:
            circuit = _new_circuit()
            gate = pq.RX(q, theta)
            return _append(circuit, gate)
        except Exception as exc:
            last_error = exc

    vqc_cls = getattr(pq, "VariationalQuantumCircuit", None)
    vrx_cls = getattr(pq, "VariationalQuantumGate_RX", None)
    if vqc_cls is not None and vrx_cls is not None:
        for theta in _parameter_candidates():
            try:
                circuit = vqc_cls()
                gate = vrx_cls(q, theta)
                return _append(circuit, gate)
            except Exception as exc:
                last_error = exc

    if last_error is not None:
        raise last_error
    raise RuntimeError("Unable to create parametrized RX circuit")
