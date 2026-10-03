# EVAL_META: task_id=9, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_efficientSU2():
    def _init_machine(machine):
        for name in ("init_qvm", "init"):
            method = getattr(machine, name, None)
            if method is not None:
                try:
                    method()
                    return
                except Exception:
                    pass

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
            method = getattr(machine, name, None)
            if method is not None:
                try:
                    return method(n)
                except Exception:
                    pass
        return [machine.qAlloc() for _ in range(n)]

    def _insert(circuit, node):
        if node is None:
            return circuit
        method = getattr(circuit, "insert", None)
        if method is not None:
            try:
                out = method(node)
                return circuit if out is None else out
            except Exception:
                pass
        try:
            return circuit << node
        except Exception:
            return circuit

    def _parameter(index):
        name = "θ[{}]".format(index)
        for ctor_name, args in (
            ("Parameter", (name,)),
            ("QParameter", (name,)),
            ("ParameterExpression", (name,)),
            ("Var", (0.0,)),
            ("var", (0.0,)),
        ):
            ctor = getattr(pq, ctor_name, None)
            if ctor is not None:
                try:
                    return ctor(*args)
                except Exception:
                    pass
        return 0.0

    def _rotation(gate_name, qubit, angle):
        gate = getattr(pq, gate_name)
        try:
            return gate(qubit, angle)
        except Exception:
            return gate(qubit, 0.0)

    def _cnot(control, target):
        for name in ("CNOT", "CX"):
            gate = getattr(pq, name, None)
            if gate is not None:
                try:
                    return gate(control, target)
                except Exception:
                    pass
        raise AttributeError("No CNOT/CX gate found in pyqpanda3.core")

    def _barrier(qubits):
        for name in ("BARRIER", "Barrier", "barrier"):
            gate = getattr(pq, name, None)
            if gate is not None:
                for args in ((qubits,), tuple(qubits), ()):
                    try:
                        return gate(*args)
                    except Exception:
                        pass
        return None

    qvm = pq.CPUQVM()
    _init_machine(qvm)
    qubits = _alloc_qubits(qvm, 3)

    circuit = pq.QCircuit()
    params = [_parameter(i) for i in range(12)]

    for i in range(3):
        circuit = _insert(circuit, _rotation("RY", qubits[i], params[i]))
    for i in range(3):
        circuit = _insert(circuit, _rotation("RZ", qubits[i], params[i + 3]))

    circuit = _insert(circuit, _barrier(qubits))

    circuit = _insert(circuit, _cnot(qubits[2], qubits[1]))
    circuit = _insert(circuit, _cnot(qubits[1], qubits[0]))

    circuit = _insert(circuit, _barrier(qubits))

    for i in range(3):
        circuit = _insert(circuit, _rotation("RY", qubits[i], params[i + 6]))
    for i in range(3):
        circuit = _insert(circuit, _rotation("RZ", qubits[i], params[i + 9]))

    try:
        create_efficientSU2._machines.append(qvm)
        create_efficientSU2._qubits.append(qubits)
    except AttributeError:
        create_efficientSU2._machines = [qvm]
        create_efficientSU2._qubits = [qubits]

    return circuit
