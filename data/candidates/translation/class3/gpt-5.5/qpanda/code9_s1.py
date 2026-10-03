# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *


def create_efficientSU2():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(3)
    else:
        q = qvm.qalloc_many(3)

    circuit = QCircuit()

    circuit << RY(q[0], 0.0) << RY(q[1], 0.0) << RY(q[2], 0.0)
    circuit << RZ(q[0], 0.0) << RZ(q[1], 0.0) << RZ(q[2], 0.0)

    barrier = globals().get("BARRIER", globals().get("Barrier", None))
    if barrier is not None:
        try:
            circuit << barrier(q)
        except Exception:
            pass

    cnot = globals().get("CNOT", globals().get("CX", None))
    circuit << cnot(q[2], q[1]) << cnot(q[1], q[0])

    if barrier is not None:
        try:
            circuit << barrier(q)
        except Exception:
            pass

    circuit << RY(q[0], 0.0) << RY(q[1], 0.0) << RY(q[2], 0.0)
    circuit << RZ(q[0], 0.0) << RZ(q[1], 0.0) << RZ(q[2], 0.0)

    create_efficientSU2._qvm = qvm
    create_efficientSU2._qubits = q
    return circuit
