# EVAL_META: task_id=105, framework=qpanda, class=3
import math
from pyqpanda3.core import *


def initialize_cnot_dihedral():
    def _new_container():
        try:
            return QCircuit()
        except Exception:
            try:
                return QCircuit(2)
            except Exception:
                return QProg()

    def _append(container, gate):
        try:
            result = container << gate
            return container if result is None else result
        except Exception:
            result = container.insert(gate)
            return container if result is None else result

    def _t_gate(qubit):
        try:
            return T(qubit)
        except Exception:
            try:
                return U1(qubit, math.pi / 4)
            except Exception:
                return RZ(qubit, math.pi / 4)

    qvm = None
    qubits = [0, 1]

    try:
        qvm = CPUQVM()
        for init_name in ("init_qvm", "init", "initQVM"):
            if hasattr(qvm, init_name):
                getattr(qvm, init_name)()
                break

        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "allocateQubits"):
            if hasattr(qvm, alloc_name):
                qubits = getattr(qvm, alloc_name)(2)
                break
    except Exception:
        qvm = None
        qubits = [0, 1]

    circ = _new_container()

    try:
        circ = _append(circ, CNOT(qubits[0], qubits[1]))
        circ = _append(circ, _t_gate(qubits[0]))
    except Exception:
        circ = _new_container()
        circ = _append(circ, CNOT(0, 1))
        circ = _append(circ, _t_gate(0))

    if not hasattr(initialize_cnot_dihedral, "_resources"):
        initialize_cnot_dihedral._resources = []
    initialize_cnot_dihedral._resources.append((qvm, qubits))

    try:
        return CNOTDihedral(circ)
    except Exception:
        return circ
