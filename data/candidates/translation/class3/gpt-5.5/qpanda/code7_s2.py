# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import *

def create_parametrized_gate():
    def _parameter_candidates():
        candidates = []
        for name in ("Parameter", "PVar", "Var", "Variable", "AngleParameter", "ParameterExpression"):
            cls = globals().get(name)
            if cls is None:
                continue
            for args in (("theta",), ("theta", 0.0), (0.0, "theta"), (0.0,)):
                try:
                    candidates.append(cls(*args))
                    break
                except Exception:
                    pass
        var_fn = globals().get("var")
        if var_fn is not None:
            for args in (("theta",), (0.0, True), (0.0,)):
                try:
                    candidates.append(var_fn(*args))
                    break
                except Exception:
                    pass
        candidates.append("theta")
        return candidates

    def _new_circuit():
        for name in ("QCircuit", "QuantumCircuit", "QProg"):
            cls = globals().get(name)
            if cls is None:
                continue
            for args in ((1,), ()):
                try:
                    return cls(*args)
                except Exception:
                    pass
        raise RuntimeError("No pyQPanda3 circuit/program class is available")

    def _append_gate(circuit, gate):
        try:
            result = circuit << gate
            return circuit if result is None else result
        except Exception:
            pass
        for method_name in ("insert", "append", "add_gate", "push_back"):
            method = getattr(circuit, method_name, None)
            if method is None:
                continue
            try:
                result = method(gate)
                return circuit if result is None else result
            except Exception:
                pass
        raise RuntimeError("Unable to append RX gate to pyQPanda3 circuit")

    def _allocate_qubit():
        machine = None
        cpu_qvm_cls = globals().get("CPUQVM")
        if cpu_qvm_cls is not None:
            machine = cpu_qvm_cls()
            for method_name in ("init_qvm", "initQVM", "init"):
                method = getattr(machine, method_name, None)
                if method is not None:
                    try:
                        method()
                    except Exception:
                        pass
        elif globals().get("init_quantum_machine") is not None and globals().get("QMachineType") is not None:
            try:
                machine = init_quantum_machine(QMachineType.CPU)
            except Exception:
                machine = None
        if machine is None:
            raise RuntimeError("Unable to allocate a pyQPanda3 qubit")
        for method_name in ("qAlloc", "qalloc", "allocate_qubit"):
            method = getattr(machine, method_name, None)
            if method is not None:
                try:
                    qubit = method()
                    if not hasattr(create_parametrized_gate, "_machines"):
                        create_parametrized_gate._machines = []
                    create_parametrized_gate._machines.append(machine)
                    return qubit
                except Exception:
                    pass
        for method_name in ("qAlloc_many", "qalloc_many", "allocate_qubits"):
            method = getattr(machine, method_name, None)
            if method is not None:
                try:
                    qubits = method(1)
                    if not hasattr(create_parametrized_gate, "_machines"):
                        create_parametrized_gate._machines = []
                    create_parametrized_gate._machines.append(machine)
                    return qubits[0]
                except Exception:
                    pass
        raise RuntimeError("Unable to allocate a pyQPanda3 qubit")

    rx_fn = globals().get("RX") or globals().get("rx")
    if rx_fn is None:
        raise RuntimeError("RX gate is not available in pyQPanda3")

    params = _parameter_candidates()
    circuit = _new_circuit()

    for theta in params:
        for gate_args in ((0, theta), (theta, 0)):
            try:
                gate = rx_fn(*gate_args)
                return _append_gate(circuit, gate)
            except Exception:
                pass

    qubit = _allocate_qubit()
    circuit = _new_circuit()
    for theta in params:
        try:
            gate = rx_fn(qubit, theta)
            return _append_gate(circuit, gate)
        except Exception:
            pass

    vqc_cls = globals().get("VariationalQuantumCircuit")
    vrx_cls = globals().get("VariationalQuantumGate_RX")
    if vqc_cls is not None and vrx_cls is not None:
        qubit = _allocate_qubit()
        vqc = vqc_cls()
        for theta in params:
            try:
                gate = vrx_cls(qubit, theta)
                result = vqc.insert(gate)
                return vqc if result is None else result
            except Exception:
                pass

    raise RuntimeError("Unable to create a parametrized RX gate circuit")
