# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq

def rx_gate(value=None):
    def _make_parameter():
        for name in ("Parameter", "QParameter", "ParameterExpression", "Var", "Variable"):
            cls = getattr(pq, name, None)
            if cls is not None:
                for args in (("theta",),):
                    try:
                        return cls(*args)
                    except Exception:
                        pass
        var_fn = getattr(pq, "var", None)
        if var_fn is not None:
            for args in (("theta",), (0.0,)):
                try:
                    return var_fn(*args)
                except Exception:
                    pass
        return "theta"

    def _make_circuit():
        cls = getattr(pq, "QCircuit", None)
        if cls is not None:
            for args in ((1,), ()):
                try:
                    return cls(*args)
                except Exception:
                    pass
        cls = getattr(pq, "QProg")
        for args in ((1,), ()):
            try:
                return cls(*args)
            except Exception:
                pass
        return cls()

    def _append(container, gate):
        for method_name in ("insert", "append", "add_gate"):
            method = getattr(container, method_name, None)
            if method is not None:
                try:
                    result = method(gate)
                    return container if result is None else result
                except Exception:
                    pass
        result = container << gate
        return container if result is None else result

    def _alloc_qubit():
        machine = pq.CPUQVM()
        for method_name in ("init_qvm", "init", "initQVM"):
            method = getattr(machine, method_name, None)
            if method is not None:
                try:
                    method()
                    break
                except Exception:
                    pass
        for method_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
            method = getattr(machine, method_name, None)
            if method is not None:
                try:
                    qubits = method(1)
                    if not hasattr(rx_gate, "_machines"):
                        rx_gate._machines = []
                    rx_gate._machines.append(machine)
                    return qubits[0]
                except Exception:
                    pass
        for method_name in ("qAlloc", "qalloc", "allocate_qubit"):
            method = getattr(machine, method_name, None)
            if method is not None:
                try:
                    qubit = method()
                    if not hasattr(rx_gate, "_machines"):
                        rx_gate._machines = []
                    rx_gate._machines.append(machine)
                    return qubit
                except Exception:
                    pass
        raise RuntimeError("Unable to allocate a pyQPanda qubit")

    angle = value if value is not None else _make_parameter()
    circuit = _make_circuit()

    rx = getattr(pq, "RX")
    gate = None
    for qubit in (0,):
        for args in ((qubit, angle), (angle, qubit)):
            try:
                gate = rx(*args)
                break
            except Exception:
                pass
        if gate is not None:
            break

    if gate is None:
        qubit = _alloc_qubit()
        for args in ((qubit, angle), (angle, qubit)):
            try:
                gate = rx(*args)
                break
            except Exception:
                pass

    if gate is None:
        raise RuntimeError("Unable to construct RX gate in pyQPanda3")

    return _append(circuit, gate)
