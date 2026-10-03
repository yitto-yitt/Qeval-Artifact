# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import *


def create_state_prep():
    def _append(circuit, op):
        try:
            circuit << op
        except Exception:
            circuit.insert(op)
        return circuit

    def _add_idle(circuit, qubit):
        try:
            _append(circuit, I(qubit))
        except Exception:
            try:
                _append(circuit, H(qubit))
                _append(circuit, H(qubit))
            except Exception:
                pass

    try:
        qc = QCircuit(2)
        _append(qc, X(0))
        _add_idle(qc, 1)
        return qc
    except Exception:
        pass

    try:
        qc = QCircuit()
        _append(qc, X(0))
        _add_idle(qc, 1)
        return qc
    except Exception:
        pass

    qvm = CPUQVM()
    for name in ("init_qvm", "init", "initQVM"):
        try:
            method = getattr(qvm, name)
            method()
            break
        except Exception:
            pass

    qubits = None
    for name in ("qAlloc_many", "qalloc_many", "q_alloc_many", "alloc_many", "allocate_qubits"):
        try:
            qubits = getattr(qvm, name)(2)
            break
        except Exception:
            pass

    if qubits is None:
        qubits = []
        for name in ("qAlloc", "qalloc", "q_alloc", "allocate_qubit"):
            try:
                alloc = getattr(qvm, name)
                qubits = [alloc(), alloc()]
                break
            except Exception:
                pass

    qc = QCircuit()
    _append(qc, X(qubits[0]))
    _add_idle(qc, qubits[1])

    create_state_prep._qvm = qvm
    create_state_prep._qubits = qubits
    return qc
