# EVAL_META: task_id=65, framework=qpanda, class=3
from math import pi
import pyqpanda3.core as pq

def QFT(n):
    def _new_container():
        cls = getattr(pq, "QCircuit", None)
        if cls is not None:
            try:
                return cls()
            except Exception:
                pass
        return pq.QProg()

    def _append(container, node):
        try:
            r = container << node
            return container if r is None else r
        except Exception:
            pass
        for name in ("insert", "append", "push_back"):
            f = getattr(container, name, None)
            if f is not None:
                r = f(node)
                return container if r is None else r
        raise RuntimeError("Unable to append node to pyQPanda3 circuit/program")

    def _init_machine():
        for cls_name in ("CPUQVM", "CPUSingleThreadQVM", "QMachine", "QuantumMachine"):
            cls = getattr(pq, cls_name, None)
            if cls is None:
                continue
            try:
                machine = cls()
                for init_name in ("init_qvm", "init", "initQVM"):
                    init_fn = getattr(machine, init_name, None)
                    if init_fn is not None:
                        try:
                            init_fn()
                            break
                        except TypeError:
                            try:
                                init_fn("")
                                break
                            except Exception:
                                pass
                        except Exception:
                            pass
                return machine
            except Exception:
                pass
        return None

    def _alloc_qubits(count):
        machine = _init_machine()
        if machine is not None:
            for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "allocate_qubits"):
                f = getattr(machine, name, None)
                if f is not None:
                    try:
                        qv = f(count)
                        if not hasattr(QFT, "_qpanda_machines"):
                            QFT._qpanda_machines = []
                        QFT._qpanda_machines.append(machine)
                        return qv
                    except Exception:
                        pass
            for single_name in ("qAlloc", "qalloc", "allocate_qubit"):
                f = getattr(machine, single_name, None)
                if f is not None:
                    try:
                        qv = [f() for _ in range(count)]
                        if not hasattr(QFT, "_qpanda_machines"):
                            QFT._qpanda_machines = []
                        QFT._qpanda_machines.append(machine)
                        return qv
                    except Exception:
                        pass
        for init_name in ("init", "init_qvm", "initQVM"):
            f = getattr(pq, init_name, None)
            if f is not None:
                try:
                    f()
                    break
                except Exception:
                    pass
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            f = getattr(pq, name, None)
            if f is not None:
                try:
                    return f(count)
                except Exception:
                    pass
        f = getattr(pq, "qAlloc", None) or getattr(pq, "qalloc", None)
        if f is not None:
            return [f() for _ in range(count)]
        raise RuntimeError("Unable to allocate qubits in pyQPanda3")

    def _gate(name_list, *args):
        last_exc = None
        for name in name_list:
            f = getattr(pq, name, None)
            if f is None:
                continue
            try:
                return f(*args)
            except Exception as exc:
                last_exc = exc
        if last_exc is not None:
            raise last_exc
        raise AttributeError("Missing gate: " + str(name_list))

    circuit = _new_container()
    q = _alloc_qubits(n) if n > 0 else []

    def _add_h(qb):
        nonlocal circuit
        circuit = _append(circuit, _gate(("H", "Hadamard"), qb))

    def _add_cnot(ctrl, targ):
        nonlocal circuit
        circuit = _append(circuit, _gate(("CNOT", "CX"), ctrl, targ))

    def _add_phase(qb, angle):
        nonlocal circuit
        for name in ("P", "Phase", "PHASE", "U1"):
            f = getattr(pq, name, None)
            if f is not None:
                try:
                    circuit = _append(circuit, f(qb, angle))
                    return True
                except Exception:
                    try:
                        circuit = _append(circuit, f(angle, qb))
                        return True
                    except Exception:
                        pass
        f = getattr(pq, "RZ", None)
        if f is not None:
            circuit = _append(circuit, f(qb, angle))
            return True
        return False

    def _add_cp(ctrl, targ, angle):
        nonlocal circuit
        for name in ("CP", "CPhase", "CPHASE", "CR"):
            f = getattr(pq, name, None)
            if f is not None:
                try:
                    circuit = _append(circuit, f(ctrl, targ, angle))
                    return
                except Exception:
                    try:
                        circuit = _append(circuit, f(angle, ctrl, targ))
                        return
                    except Exception:
                        pass
        phase_available = any(getattr(pq, name, None) is not None for name in ("P", "Phase", "PHASE", "U1"))
        if phase_available:
            _add_phase(ctrl, angle / 2)
            _add_phase(targ, angle / 2)
            _add_cnot(ctrl, targ)
            _add_phase(targ, -angle / 2)
            _add_cnot(ctrl, targ)
        else:
            circuit = _append(circuit, _gate(("RZ",), ctrl, angle / 2))
            _add_cnot(ctrl, targ)
            circuit = _append(circuit, _gate(("RZ",), targ, -angle / 2))
            _add_cnot(ctrl, targ)
            circuit = _append(circuit, _gate(("RZ",), targ, angle / 2))

    def _add_swap(a, b):
        nonlocal circuit
        for name in ("SWAP", "Swap"):
            f = getattr(pq, name, None)
            if f is not None:
                try:
                    circuit = _append(circuit, f(a, b))
                    return
                except Exception:
                    pass
        _add_cnot(a, b)
        _add_cnot(b, a)
        _add_cnot(a, b)

    def qft_rotations(m):
        if m == 0:
            return
        m -= 1
        _add_h(q[m])
        for qubit in range(m):
            _add_cp(q[qubit], q[m], pi / (2 ** (m - qubit)))
        qft_rotations(m)

    qft_rotations(n)
    for qubit in range(n // 2):
        _add_swap(q[qubit], q[n - qubit - 1])

    QFT._last_qubits = q
    return circuit
