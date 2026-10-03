# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq

def rx_gate(value=None):
    if not hasattr(rx_gate, "_machines"):
        rx_gate._machines = []

    def _unique_append(items, obj):
        if not any(obj is x for x in items):
            items.append(obj)

    def _angle_candidates():
        angles = []
        if value is not None:
            _unique_append(angles, value)
            try:
                _unique_append(angles, float(value))
            except Exception:
                pass
            return angles

        constructors = [
            ("Parameter", [("theta",)]),
            ("ParameterExpression", [("theta",)]),
            ("Expression", [("theta",)]),
            ("Var", [("theta",), (0.0, "theta"), ("theta", 0.0), (0.0,)]),
            ("var", [("theta",), (0.0, "theta"), ("theta", 0.0), (0.0, True), (0.0,)]),
            ("angle_var", [("theta",), (0.0, "theta"), ("theta", 0.0), (0.0,)]),
        ]
        for name, arglists in constructors:
            ctor = getattr(pq, name, None)
            if ctor is None:
                continue
            for args in arglists:
                try:
                    obj = ctor(*args)
                    for setter in ("set_name", "setName", "set_var_name", "setVarName"):
                        try:
                            getattr(obj, setter)("theta")
                        except Exception:
                            pass
                    _unique_append(angles, obj)
                except Exception:
                    pass
        _unique_append(angles, "theta")
        return angles

    def _qubit_candidates():
        qubits = [0]
        qbit_cls = getattr(pq, "Qubit", None)
        if qbit_cls is not None:
            for args in ((0,),):
                try:
                    _unique_append(qubits, qbit_cls(*args))
                except Exception:
                    pass

        for machine_name in ("CPUQVM", "CPUMachine", "QuantumMachine", "QVM"):
            machine_cls = getattr(pq, machine_name, None)
            if machine_cls is None:
                continue
            try:
                machine = machine_cls()
            except Exception:
                continue
            for init_name in ("init_qvm", "initQVM", "init", "init_qvm_with_config"):
                try:
                    getattr(machine, init_name)()
                except Exception:
                    pass
            for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "alloc_qubits"):
                try:
                    qs = getattr(machine, alloc_name)(1)
                    q = qs[0]
                    rx_gate._machines.append(machine)
                    _unique_append(qubits, q)
                except Exception:
                    pass
            for alloc_name in ("qAlloc", "qalloc", "alloc_qubit"):
                for args in ((), (0,)):
                    try:
                        q = getattr(machine, alloc_name)(*args)
                        rx_gate._machines.append(machine)
                        _unique_append(qubits, q)
                    except Exception:
                        pass
        return qubits

    def _container_candidates():
        out = []
        for name in ("QCircuit", "QProg"):
            cls = getattr(pq, name, None)
            if cls is None:
                continue
            for args in ((), (1,)):
                try:
                    out.append(cls(*args))
                except Exception:
                    pass
        return out

    last_error = None
    rx_ctor = getattr(pq, "RX", None)
    if rx_ctor is not None:
        for angle in _angle_candidates():
            for qubit in _qubit_candidates():
                try:
                    gate = rx_ctor(qubit, angle)
                except Exception as exc:
                    last_error = exc
                    continue
                for container in _container_candidates():
                    try:
                        result = container << gate
                        return result if result is not None and not isinstance(result, bool) else container
                    except Exception as exc:
                        last_error = exc
                    for method_name in ("insert", "append", "add_gate", "push_back"):
                        try:
                            result = getattr(container, method_name)(gate)
                            return result if result is not None and not isinstance(result, bool) else container
                        except Exception as exc:
                            last_error = exc

    vqc_cls = getattr(pq, "VariationalQuantumCircuit", None)
    vgate_cls = getattr(pq, "VariationalQuantumGate_RX", None)
    var_ctor = getattr(pq, "var", None)
    if vqc_cls is not None and vgate_cls is not None and var_ctor is not None:
        for qubit in _qubit_candidates():
            try:
                theta = var_ctor(float(value) if value is not None else 0.0, True)
            except Exception:
                try:
                    theta = var_ctor(float(value) if value is not None else 0.0)
                except Exception as exc:
                    last_error = exc
                    continue
            for setter in ("set_name", "setName", "set_var_name", "setVarName"):
                try:
                    getattr(theta, setter)("theta")
                except Exception:
                    pass
            try:
                gate = vgate_cls(qubit, theta)
                circuit = vqc_cls()
                result = circuit.insert(gate)
                return result if result is not None and not isinstance(result, bool) else circuit
            except Exception as exc:
                last_error = exc

    if last_error is not None:
        raise last_error
    raise RuntimeError("Unable to construct RX gate circuit in pyqpanda3")
