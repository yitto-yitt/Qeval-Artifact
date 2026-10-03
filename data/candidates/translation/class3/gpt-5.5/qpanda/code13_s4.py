# EVAL_META: task_id=13, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def custom_rotation_gate():
    theta = math.pi / 2
    phi = math.pi / 2
    lam = math.pi / 2

    def _new_circuit():
        for name in ("QCircuit", "Circuit", "QProg"):
            cls = getattr(pq, name, None)
            if cls is not None:
                try:
                    return cls()
                except TypeError:
                    try:
                        return cls(1)
                    except TypeError:
                        pass
        raise RuntimeError("No circuit/program class available in pyqpanda3.core")

    def _append(circuit, op):
        try:
            result = circuit << op
            return circuit if result is None else result
        except Exception:
            if hasattr(circuit, "insert"):
                result = circuit.insert(op)
                return circuit if result is None else result
            if hasattr(circuit, "append"):
                result = circuit.append(op)
                return circuit if result is None else result
            raise

    def _make_u(q):
        for name in ("U3", "U"):
            gate_fn = getattr(pq, name, None)
            if gate_fn is not None:
                try:
                    return gate_fn(q, theta, phi, lam)
                except Exception:
                    pass
        return None

    def _build(q):
        circuit = _new_circuit()
        gate = _make_u(q)
        if gate is not None:
            return _append(circuit, gate)
        circuit = _append(circuit, pq.RZ(q, lam))
        circuit = _append(circuit, pq.RY(q, theta))
        circuit = _append(circuit, pq.RZ(q, phi))
        return circuit

    try:
        return _build(0)
    except Exception:
        machine = pq.CPUQVM()
        for init_name in ("init_qvm", "init"):
            init_fn = getattr(machine, init_name, None)
            if init_fn is not None:
                try:
                    init_fn()
                except Exception:
                    pass
                break

        qubits = None
        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            alloc_fn = getattr(machine, alloc_name, None)
            if alloc_fn is not None:
                qubits = alloc_fn(1)
                break
        if qubits is None:
            for alloc_name in ("qAlloc", "qalloc"):
                alloc_fn = getattr(machine, alloc_name, None)
                if alloc_fn is not None:
                    qubits = [alloc_fn()]
                    break
        if qubits is None:
            raise RuntimeError("No qubit allocation method available in pyqpanda3.core")

        custom_rotation_gate._machine = machine
        custom_rotation_gate._qubits = qubits
        return _build(qubits[0])
