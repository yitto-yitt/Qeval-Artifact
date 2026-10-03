# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import *

def create_cy_gate():
    def _circuit_type():
        cls = globals().get("QCircuit", None)
        if cls is not None:
            return cls
        return globals()["QProg"]

    def _cx_gate(q0, q1):
        gate_fn = globals().get("CNOT", None)
        if gate_fn is None:
            gate_fn = globals()["CX"]
        return gate_fn(q0, q1)

    def _sdg_gate(q):
        for name in ("Sdag", "Sdg", "SDG", "S_DAG"):
            gate_fn = globals().get(name, None)
            if gate_fn is not None:
                return gate_fn(q)
        gate = S(q)
        for name in ("dagger", "Dagger", "inverse", "adjoint"):
            method = getattr(gate, name, None)
            if method is not None:
                if callable(method):
                    result = method()
                    return gate if result is None else result
                return method
        return gate.dagger()

    def _add(container, op):
        try:
            result = container << op
            return container if result is None else result
        except Exception:
            result = container.insert(op)
            return container if result is None else result

    def _build(q0, q1):
        circuit = _circuit_type()()
        circuit = _add(circuit, _sdg_gate(q1))
        circuit = _add(circuit, _cx_gate(q0, q1))
        circuit = _add(circuit, S(q1))
        return circuit

    try:
        return _build(0, 1)
    except Exception:
        machine = CPUQVM()
        for name in ("init_qvm", "initQVM", "init"):
            method = getattr(machine, name, None)
            if method is not None:
                try:
                    method()
                except Exception:
                    pass
                break

        qubits = None
        for name in ("qAlloc_many", "qAllocMany", "qalloc_many", "qallocMany"):
            method = getattr(machine, name, None)
            if method is not None:
                qubits = method(2)
                break

        if qubits is None:
            alloc = getattr(machine, "qAlloc")
            qubits = [alloc(), alloc()]

        if not hasattr(create_cy_gate, "_qpanda_machines"):
            create_cy_gate._qpanda_machines = []
        create_cy_gate._qpanda_machines.append(machine)

        return _build(qubits[0], qubits[1])
