# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def decompose_unitary(unitary):
    mat = np.asarray(unitary.data if hasattr(unitary, "data") else unitary, dtype=np.complex128)

    def _make_machine_and_qubits():
        machine_cls = (
            globals().get("CPUQVM")
            or globals().get("CPUSingleThreadQVM")
            or globals().get("QuantumMachine")
        )
        machine = machine_cls()
        for name in ("init_qvm", "init", "initialize"):
            if hasattr(machine, name):
                try:
                    getattr(machine, name)()
                    break
                except TypeError:
                    pass

        qv = None
        for name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "qAllocMany"):
            if hasattr(machine, name):
                qv = getattr(machine, name)(2)
                break
        if qv is None:
            for name in ("qAlloc", "qalloc", "allocate_qubit"):
                if hasattr(machine, name):
                    qv = [getattr(machine, name)() for _ in range(2)]
                    break

        if not hasattr(decompose_unitary, "_machines"):
            decompose_unitary._machines = []
        decompose_unitary._machines.append(machine)
        return machine, qv

    def _new_circuit():
        try:
            return QCircuit()
        except Exception:
            return QProg()

    def _gate(names, *args):
        last = None
        for name in names:
            fn = globals().get(name)
            if fn is None:
                continue
            try:
                return fn(*args)
            except Exception as exc:
                last = exc
        if last is not None:
            raise last
        raise RuntimeError("gate not available")

    def _append(circ, gate):
        circ << gate
        return circ

    def _append_u(circ, q, theta, phi, lam):
        try:
            return _append(circ, _gate(("U3", "U"), q, theta, phi, lam))
        except Exception:
            _append(circ, _gate(("RZ",), q, lam))
            _append(circ, _gate(("RY",), q, theta))
            _append(circ, _gate(("RZ",), q, phi))
            return circ

    def _dagger_gate(g):
        for name in ("dagger", "inverse"):
            if hasattr(g, name):
                r = getattr(g, name)()
                return g if r is None else r
        if hasattr(g, "set_dagger"):
            g.set_dagger(True)
            return g
        return g

    machine, qv = _make_machine_and_qubits()

    try:
        from qiskit.synthesis import TwoQubitBasisDecomposer
        from qiskit.circuit.library import CXGate

        qc = TwoQubitBasisDecomposer(CXGate())(mat)
        circ = _new_circuit()

        for item in qc.data:
            op = getattr(item, "operation", item[0])
            qargs = getattr(item, "qubits", item[1])
            name = op.name.lower()
            idx = [qc.find_bit(qb).index if hasattr(qc, "find_bit") else qb.index for qb in qargs]
            params = [float(p) for p in getattr(op, "params", [])]

            if name in ("cx", "cnot"):
                _append(circ, _gate(("CNOT", "CX"), qv[idx[0]], qv[idx[1]]))
            elif name in ("u", "u3"):
                _append_u(circ, qv[idx[0]], params[0], params[1], params[2])
            elif name == "u2":
                _append_u(circ, qv[idx[0]], np.pi / 2, params[0], params[1])
            elif name in ("u1", "p"):
                try:
                    _append(circ, _gate(("U1", "P"), qv[idx[0]], params[0]))
                except Exception:
                    _append(circ, _gate(("RZ",), qv[idx[0]], params[0]))
            elif name == "rz":
                _append(circ, _gate(("RZ",), qv[idx[0]], params[0]))
            elif name == "ry":
                _append(circ, _gate(("RY",), qv[idx[0]], params[0]))
            elif name == "rx":
                _append(circ, _gate(("RX",), qv[idx[0]], params[0]))
            elif name == "x":
                _append(circ, _gate(("X",), qv[idx[0]]))
            elif name == "y":
                _append(circ, _gate(("Y",), qv[idx[0]]))
            elif name == "z":
                _append(circ, _gate(("Z",), qv[idx[0]]))
            elif name == "h":
                _append(circ, _gate(("H",), qv[idx[0]]))
            elif name == "s":
                _append(circ, _gate(("S",), qv[idx[0]]))
            elif name == "sdg":
                _append(circ, _dagger_gate(_gate(("S",), qv[idx[0]])))
            elif name == "t":
                _append(circ, _gate(("T",), qv[idx[0]]))
            elif name == "tdg":
                _append(circ, _dagger_gate(_gate(("T",), qv[idx[0]])))
            elif name in ("id", "delay", "barrier"):
                pass
            else:
                raise RuntimeError("unsupported gate")
        return circ
    except Exception:
        pass

    for fname in ("matrix_decompose", "MatrixDecompose", "matrix_decomposition"):
        fn = globals().get(fname)
        if fn is None:
            continue
        for qs in (qv, list(qv)):
            for m in (mat, mat.tolist()):
                for args in ((qs, m), (m, qs)):
                    try:
                        return fn(*args)
                    except Exception:
                        pass

    circ = _new_circuit()
    for fname in ("QOracle", "Oracle", "Unitary", "U4"):
        fn = globals().get(fname)
        if fn is None:
            continue
        for qs in (qv, list(qv)):
            for m in (mat, mat.tolist()):
                for args in ((qs, m), (m, qs)):
                    try:
                        return _append(circ, fn(*args))
                    except Exception:
                        pass

    raise RuntimeError("unable to decompose unitary")
