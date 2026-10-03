# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *
import pyqpanda3.core as pq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    pauli_string = str(pauli_string).upper()
    n = len(pauli_string)

    def _new_container():
        cls = getattr(pq, "QCircuit", None)
        if cls is not None:
            try:
                return cls(n)
            except Exception:
                try:
                    return cls()
                except Exception:
                    pass
        cls = getattr(pq, "QProg", None)
        if cls is not None:
            try:
                return cls()
            except Exception:
                pass
        raise RuntimeError("No pyQPanda3 circuit/program container is available")

    def _append(container, op):
        try:
            result = container << op
            return container if result is None else result
        except Exception:
            ins = getattr(container, "insert", None)
            if callable(ins):
                result = ins(op)
                return container if result is None else result
            raise

    def _gate(names, *args):
        last_error = None
        for name in names:
            fn = getattr(pq, name, None)
            if callable(fn):
                try:
                    return fn(*args)
                except Exception as exc:
                    last_error = exc
        if last_error is not None:
            raise last_error
        raise RuntimeError("Required gate is not available: " + names[0])

    def _h(q):
        return _gate(("H",), q)

    def _rz(q, theta):
        return _gate(("RZ",), q, theta)

    def _cx(c, t):
        return _gate(("CNOT", "CX"), c, t)

    def _set_global_phase(container, phase):
        for name in ("set_global_phase", "setGlobalPhase"):
            method = getattr(container, name, None)
            if callable(method):
                try:
                    method(phase)
                    return
                except Exception:
                    pass
        try:
            setattr(container, "global_phase", phase)
        except Exception:
            pass

    def _build(targets):
        circuit = _new_container()
        active = []

        for pos, p in enumerate(pauli_string):
            qidx = n - 1 - pos
            q = targets[qidx]
            if p == "I":
                continue
            active.append(qidx)
            if p == "X":
                circuit = _append(circuit, _h(q))
            elif p == "Y":
                circuit = _append(circuit, _rz(q, -np.pi / 2))
                circuit = _append(circuit, _h(q))
            elif p == "Z":
                pass
            else:
                raise ValueError("Invalid Pauli character: " + p)

        if active:
            target_idx = active[-1]
            target = targets[target_idx]
            for ctrl_idx in active[:-1]:
                circuit = _append(circuit, _cx(targets[ctrl_idx], target))
            circuit = _append(circuit, _rz(target, 2.0 * time))
            for ctrl_idx in reversed(active[:-1]):
                circuit = _append(circuit, _cx(targets[ctrl_idx], target))

            for pos in range(n - 1, -1, -1):
                p = pauli_string[pos]
                q = targets[n - 1 - pos]
                if p == "X":
                    circuit = _append(circuit, _h(q))
                elif p == "Y":
                    circuit = _append(circuit, _h(q))
                    circuit = _append(circuit, _rz(q, np.pi / 2))
        else:
            _set_global_phase(circuit, -time)

        return circuit

    try:
        return _build(list(range(n)))
    except Exception as first_error:
        qvm_cls = getattr(pq, "CPUQVM", None)
        if qvm_cls is None:
            raise first_error

        qvm = qvm_cls()
        for init_name in ("init_qvm", "initQVM", "init"):
            init = getattr(qvm, init_name, None)
            if callable(init):
                try:
                    init()
                    break
                except Exception:
                    pass

        qubits = None
        for alloc_name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "allocateQubits", "qAllocMany"):
            alloc = getattr(qvm, alloc_name, None)
            if callable(alloc):
                try:
                    qubits = list(alloc(n))
                    break
                except Exception:
                    pass

        if qubits is None:
            alloc_one = getattr(qvm, "qAlloc", None)
            if callable(alloc_one):
                qubits = [alloc_one() for _ in range(n)]

        if qubits is None:
            raise first_error

        circuit = _build(qubits)
        machines = getattr(synthesize_evolution_gate, "_machines", [])
        machines.append(qvm)
        setattr(synthesize_evolution_gate, "_machines", machines)
        return circuit
