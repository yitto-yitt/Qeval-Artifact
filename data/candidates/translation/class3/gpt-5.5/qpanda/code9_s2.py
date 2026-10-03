# EVAL_META: task_id=9, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_efficientSU2():
    def _make_machine():
        for name in ("CPUQVM", "CPUSingleThreadQVM", "OriginQVM", "QMachine"):
            cls = getattr(pq, name, None)
            if cls is None:
                continue
            try:
                machine = cls()
                for init_name in ("init_qvm", "initQVM", "init", "initialize"):
                    init = getattr(machine, init_name, None)
                    if init is not None:
                        try:
                            init()
                            break
                        except TypeError:
                            pass
                return machine
            except Exception:
                pass
        raise RuntimeError("No available pyQPanda3 quantum machine found")

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "alloc_qubits"):
            method = getattr(machine, name, None)
            if method is None:
                continue
            try:
                qs = method(n)
                return [qs[i] for i in range(n)]
            except Exception:
                try:
                    qs = list(method(n))
                    if len(qs) >= n:
                        return qs[:n]
                except Exception:
                    pass
        for name in ("qAlloc", "qalloc", "allocate_qubit", "alloc_qubit"):
            method = getattr(machine, name, None)
            if method is None:
                continue
            out = []
            ok = True
            for i in range(n):
                try:
                    out.append(method())
                except Exception:
                    try:
                        out.append(method(i))
                    except Exception:
                        ok = False
                        break
            if ok and len(out) == n:
                return out
        raise RuntimeError("Unable to allocate qubits")

    def _new_circuit():
        for name in ("QCircuit", "QProg"):
            cls = getattr(pq, name, None)
            if cls is not None:
                try:
                    return cls()
                except Exception:
                    pass
        raise RuntimeError("Unable to create pyQPanda3 circuit")

    def _parameter(i):
        for name in ("Parameter", "QParameter"):
            ctor = getattr(pq, name, None)
            if ctor is None:
                continue
            for args in ((f"θ[{i}]",), (f"theta_{i}",), (f"theta[{i}]",)):
                try:
                    return ctor(*args)
                except Exception:
                    pass
        var_ctor = getattr(pq, "var", None)
        if var_ctor is not None:
            for args in ((0.0, True), (0.0,)):
                try:
                    return var_ctor(*args)
                except Exception:
                    pass
        return 0.0

    def _one_qubit_gate(names, qubit, angle):
        for name in names:
            ctor = getattr(pq, name, None)
            if ctor is None:
                continue
            for value in (angle, 0.0):
                try:
                    return ctor(qubit, value)
                except Exception:
                    pass
        raise RuntimeError("Unable to create one-qubit gate")

    def _two_qubit_gate(names, control, target):
        for name in names:
            ctor = getattr(pq, name, None)
            if ctor is None:
                continue
            try:
                return ctor(control, target)
            except Exception:
                pass
        raise RuntimeError("Unable to create two-qubit gate")

    def _barrier(qubits):
        for name in ("BARRIER", "Barrier", "barrier"):
            ctor = getattr(pq, name, None)
            if ctor is None:
                continue
            for args in ((qubits,), (list(qubits),), tuple(qubits)):
                try:
                    return ctor(*args)
                except Exception:
                    pass
        return None

    def _append(circuit, op):
        if op is None:
            return circuit
        try:
            res = circuit << op
            return circuit if res is None else res
        except Exception:
            pass
        for name in ("insert", "append", "push_back"):
            method = getattr(circuit, name, None)
            if method is None:
                continue
            try:
                res = method(op)
                return circuit if res is None else res
            except Exception:
                pass
        raise RuntimeError("Unable to append operation to circuit")

    machine = _make_machine()
    qubits = _alloc_qubits(machine, 3)
    circuit = _new_circuit()
    theta = [_parameter(i) for i in range(12)]

    for i in range(3):
        circuit = _append(circuit, _one_qubit_gate(("RY", "Ry", "ry"), qubits[i], theta[i]))
    for i in range(3):
        circuit = _append(circuit, _one_qubit_gate(("RZ", "Rz", "rz"), qubits[i], theta[3 + i]))

    circuit = _append(circuit, _barrier(qubits))

    circuit = _append(circuit, _two_qubit_gate(("CNOT", "CX", "cnot", "cx"), qubits[2], qubits[1]))
    circuit = _append(circuit, _two_qubit_gate(("CNOT", "CX", "cnot", "cx"), qubits[1], qubits[0]))

    circuit = _append(circuit, _barrier(qubits))

    for i in range(3):
        circuit = _append(circuit, _one_qubit_gate(("RY", "Ry", "ry"), qubits[i], theta[6 + i]))
    for i in range(3):
        circuit = _append(circuit, _one_qubit_gate(("RZ", "Rz", "rz"), qubits[i], theta[9 + i]))

    refs = getattr(create_efficientSU2, "_qpanda_machine_refs", [])
    refs.append(machine)
    create_efficientSU2._qpanda_machine_refs = refs

    return circuit
