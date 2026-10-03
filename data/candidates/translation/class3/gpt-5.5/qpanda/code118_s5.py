# EVAL_META: task_id=118, framework=qpanda, class=3
import math
import pyqpanda3.core as pq
from pyqpanda3.core import *

def create_c3sx_circuit():
    qvm = pq.CPUQVM()
    for _init_name in ("init_qvm", "initQVM", "init"):
        if hasattr(qvm, _init_name):
            try:
                getattr(qvm, _init_name)()
                break
            except TypeError:
                pass

    qubits = None
    for _alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "alloc_qubits"):
        if hasattr(qvm, _alloc_name):
            try:
                qubits = list(getattr(qvm, _alloc_name)(4))
                break
            except Exception:
                pass

    if qubits is None:
        qubits = []
        for _single_alloc_name in ("qAlloc", "qalloc", "allocate_qubit", "alloc_qubit"):
            if hasattr(qvm, _single_alloc_name):
                try:
                    qubits = [getattr(qvm, _single_alloc_name)() for _ in range(4)]
                    break
                except Exception:
                    pass

    if len(qubits) != 4:
        if hasattr(pq, "init"):
            try:
                pq.init()
            except Exception:
                pass
        for _alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany"):
            if hasattr(pq, _alloc_name):
                qubits = list(getattr(pq, _alloc_name)(4))
                break

    def _controlled(gate, controls):
        for _method_name in ("control", "set_control"):
            if hasattr(gate, _method_name):
                _method = getattr(gate, _method_name)
                for _args in ((list(controls),), (tuple(controls),), (controls,), tuple(controls)):
                    try:
                        _res = _method(*_args)
                        return gate if _res is None else _res
                    except Exception:
                        pass
        raise RuntimeError("controlled gates are not supported by this pyQPanda3 installation")

    def _append(container, op):
        try:
            container << op
            return container
        except Exception:
            pass
        for _method_name in ("insert", "append", "push_back"):
            if hasattr(container, _method_name):
                try:
                    getattr(container, _method_name)(op)
                    return container
                except Exception:
                    pass
        raise RuntimeError("unable to append operation to pyQPanda3 program")

    prog = pq.QProg()

    applied = False
    if hasattr(pq, "SX"):
        try:
            _append(prog, _controlled(pq.SX(qubits[3]), [qubits[0], qubits[1], qubits[2]]))
            applied = True
        except Exception:
            applied = False

    if not applied:
        phase_gate = None
        for _phase_name in ("U1", "P", "Phase", "PHASE"):
            if hasattr(pq, _phase_name):
                try:
                    phase_gate = getattr(pq, _phase_name)(qubits[2], math.pi / 4)
                    break
                except Exception:
                    pass
        if phase_gate is None and hasattr(pq, "U3"):
            phase_gate = pq.U3(qubits[2], 0.0, 0.0, math.pi / 4)

        rx_gate = None
        if hasattr(pq, "RX"):
            rx_gate = pq.RX(qubits[3], math.pi / 2)
        elif hasattr(pq, "X1"):
            rx_gate = pq.X1(qubits[3])

        _append(prog, _controlled(phase_gate, [qubits[0], qubits[1]]))
        _append(prog, _controlled(rx_gate, [qubits[0], qubits[1], qubits[2]]))

    if not hasattr(create_c3sx_circuit, "_keepalive"):
        create_c3sx_circuit._keepalive = []
    create_c3sx_circuit._keepalive.append((qvm, qubits))

    return prog
