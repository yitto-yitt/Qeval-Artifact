# EVAL_META: task_id=44, framework=qpanda, class=3
import pyqpanda3.core as pq

def tensor_circuits():
    def _new_container():
        if hasattr(pq, "QCircuit"):
            try:
                return pq.QCircuit()
            except Exception:
                pass
        return pq.QProg()

    def _append(container, op):
        if hasattr(container, "insert"):
            result = container.insert(op)
            return container if result is None else result
        result = container << op
        return container if result is None else result

    def _cx(control, target):
        if hasattr(pq, "CNOT"):
            return pq.CNOT(control, target)
        return pq.CX(control, target)

    def _controlled_ry(control, target, angle):
        gate = pq.RY(target, angle)
        for method_name in ("control", "set_control", "setControl"):
            if hasattr(gate, method_name):
                method = getattr(gate, method_name)
                args = []
                if hasattr(pq, "QVec"):
                    try:
                        args.append(pq.QVec([control]))
                    except Exception:
                        pass
                args.extend(([control], control))
                for arg in args:
                    try:
                        controlled = method(arg)
                        return gate if controlled is None else controlled
                    except Exception:
                        pass
        if hasattr(pq, "CRY"):
            return pq.CRY(control, target, angle)
        raise AttributeError("No controlled RY construction available")

    def _build(q0, q1, q2):
        circuit = _new_container()
        try:
            circuit = _append(circuit, _controlled_ry(q0, q1, 0.2))
        except Exception:
            circuit = _append(circuit, pq.RY(q1, 0.1))
            circuit = _append(circuit, _cx(q0, q1))
            circuit = _append(circuit, pq.RY(q1, -0.1))
            circuit = _append(circuit, _cx(q0, q1))
        circuit = _append(circuit, pq.X(q2))
        return circuit

    try:
        return _build(0, 1, 2)
    except Exception:
        machine = pq.CPUQVM()
        if hasattr(machine, "init_qvm"):
            machine.init_qvm()
        elif hasattr(machine, "init"):
            machine.init()

        if hasattr(machine, "qAlloc_many"):
            qubits = machine.qAlloc_many(3)
        elif hasattr(machine, "qalloc_many"):
            qubits = machine.qalloc_many(3)
        elif hasattr(machine, "allocate_qubits"):
            qubits = machine.allocate_qubits(3)
        else:
            qubits = [machine.qAlloc() for _ in range(3)]

        circuit = _build(qubits[0], qubits[1], qubits[2])
        try:
            setattr(circuit, "_qvm", machine)
        except Exception:
            setattr(tensor_circuits, "_qvm", machine)
        return circuit
