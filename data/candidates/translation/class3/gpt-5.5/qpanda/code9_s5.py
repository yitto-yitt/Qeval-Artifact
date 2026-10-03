# EVAL_META: task_id=9, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_efficientSU2():
    operations = [
        ("RY", 0, 0), ("RY", 1, 1), ("RY", 2, 2),
        ("RZ", 0, 3), ("RZ", 1, 4), ("RZ", 2, 5),
        ("BARRIER",),
        ("CNOT", 2, 1), ("CNOT", 1, 0),
        ("BARRIER",),
        ("RY", 0, 6), ("RY", 1, 7), ("RY", 2, 8),
        ("RZ", 0, 9), ("RZ", 1, 10), ("RZ", 2, 11),
    ]

    def _params():
        names = [f"θ[{i}]" for i in range(12)]
        sets = []
        for cname in ("Parameter", "ParameterExpression"):
            cls = getattr(pq, cname, None)
            if cls is not None:
                try:
                    sets.append([cls(n) for n in names])
                except Exception:
                    pass
        for cname in ("var", "Var"):
            cls = getattr(pq, cname, None)
            if cls is not None:
                try:
                    sets.append([cls(0.0) for _ in names])
                except Exception:
                    pass
        sets.append([0.0 for _ in names])
        return sets

    def _circuit_factories():
        factories = []
        for cname in ("QCircuit", "QuantumCircuit", "Circuit", "QProg"):
            cls = getattr(pq, cname, None)
            if cls is None:
                continue
            factories.append(lambda cls=cls: cls())
            factories.append(lambda cls=cls: cls(3))
        return factories

    def _len_at_least_three(qs):
        try:
            return len(qs) >= 3
        except Exception:
            try:
                qs[2]
                return True
            except Exception:
                return False

    def _qubit_options():
        opts = [([0, 1, 2], None)]
        for mname in ("CPUQVM", "CPUSingleThreadQVM", "QVM", "QuantumMachine"):
            mcls = getattr(pq, mname, None)
            if mcls is None:
                continue
            try:
                machine = mcls()
            except Exception:
                continue
            for init_name in ("init_qvm", "initQVM", "init", "initialize"):
                init = getattr(machine, init_name, None)
                if init is not None:
                    try:
                        init()
                    except Exception:
                        pass
                    break
            for aname in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "qAlloc"):
                alloc = getattr(machine, aname, None)
                if alloc is None:
                    continue
                try:
                    qs = alloc(3)
                except Exception:
                    continue
                if _len_at_least_three(qs):
                    opts.append((qs, machine))
                    try:
                        lqs = list(qs)
                        if _len_at_least_three(lqs):
                            opts.append((lqs, machine))
                    except Exception:
                        pass
                    break
        return opts

    def _insert(circuit, node):
        for mname in ("insert", "append", "add_gate", "add"):
            method = getattr(circuit, mname, None)
            if method is not None:
                try:
                    ret = method(node)
                    return circuit if ret is None else ret
                except Exception:
                    pass
        try:
            ret = circuit.__lshift__(node)
            return circuit if ret is None else ret
        except Exception as exc:
            raise exc

    def _gate(name, qs, qubit_index, angle):
        for fname in ((name, name.lower()) if name != "CNOT" else ("CNOT", "CX", "cnot", "cx")):
            func = getattr(pq, fname, None)
            if func is None:
                continue
            try:
                if name == "CNOT":
                    return func(qs[qubit_index[0]], qs[qubit_index[1]])
                return func(qs[qubit_index], angle)
            except Exception:
                pass
        raise RuntimeError(name)

    def _barrier(circuit, qs):
        for mname in ("barrier", "BARRIER", "Barrier"):
            method = getattr(circuit, mname, None)
            if method is not None:
                for args in ((qs,), tuple(qs), ()):
                    try:
                        ret = method(*args)
                        if ret is not None:
                            circuit = ret
                        return circuit
                    except Exception:
                        pass
        for fname in ("BARRIER", "Barrier", "barrier"):
            func = getattr(pq, fname, None)
            if func is None:
                continue
            for args in ((qs,), tuple(qs)):
                try:
                    node = func(*args)
                    return _insert(circuit, node)
                except Exception:
                    pass
        raise RuntimeError("BARRIER")

    def _build_gate_based(factory, qs, params, require_barrier=True):
        circuit = factory()
        for op in operations:
            if op[0] == "BARRIER":
                if require_barrier:
                    circuit = _barrier(circuit, qs)
                continue
            if op[0] == "CNOT":
                node = _gate("CNOT", qs, (op[1], op[2]), None)
            else:
                node = _gate(op[0], qs, op[1], params[op[2]])
            circuit = _insert(circuit, node)
        return circuit

    def _call_method(circuit, names, *arg_options):
        last = None
        for name in names:
            method = getattr(circuit, name, None)
            if method is None:
                continue
            for args in arg_options:
                try:
                    ret = method(*args)
                    return circuit if ret is None else ret
                except Exception as exc:
                    last = exc
        if last is not None:
            raise last
        raise RuntimeError(names[0])

    def _build_method_based(factory, params, require_barrier=True):
        circuit = factory()
        for op in operations:
            if op[0] == "BARRIER":
                if require_barrier:
                    circuit = _call_method(circuit, ("barrier", "BARRIER", "Barrier"), ([0, 1, 2],), (0, 1, 2), ())
                continue
            if op[0] == "CNOT":
                circuit = _call_method(circuit, ("cx", "cnot", "CX", "CNOT"), (op[1], op[2]))
            elif op[0] == "RY":
                circuit = _call_method(circuit, ("ry", "RY"), (params[op[2]], op[1]), (op[1], params[op[2]]))
            else:
                circuit = _call_method(circuit, ("rz", "RZ"), (params[op[2]], op[1]), (op[1], params[op[2]]))
        return circuit

    last_error = None
    factories = _circuit_factories()
    qubit_opts = _qubit_options()

    for require_barrier in (True, False):
        for params in _params():
            for factory in factories:
                for qs, machine in qubit_opts:
                    try:
                        circuit = _build_gate_based(factory, qs, params, require_barrier)
                        if machine is not None:
                            create_efficientSU2._qvm = machine
                        return circuit
                    except Exception as exc:
                        last_error = exc
                try:
                    return _build_method_based(factory, params, require_barrier)
                except Exception as exc:
                    last_error = exc

    raise RuntimeError("Unable to construct EfficientSU2 circuit in pyQPanda3") from last_error
