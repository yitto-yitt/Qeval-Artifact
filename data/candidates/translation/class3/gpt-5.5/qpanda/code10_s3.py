# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import *

def create_operator():
    try:
        prog = QProg()
        prog << X(0)
        prog << X(1)
        return prog
    except Exception:
        pass

    try:
        circuit = QCircuit(2)
        circuit << X(0)
        circuit << X(1)
        return circuit
    except Exception:
        pass

    try:
        circuit = QCircuit()
        circuit << X(0)
        circuit << X(1)
        return circuit
    except Exception:
        pass

    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()
    elif hasattr(qvm, "initialize"):
        qvm.initialize()

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(2)
    elif hasattr(qvm, "qalloc_many"):
        q = qvm.qalloc_many(2)
    elif hasattr(qvm, "qAllocMany"):
        q = qvm.qAllocMany(2)
    elif hasattr(qvm, "allocate_qubits"):
        q = qvm.allocate_qubits(2)
    elif hasattr(qvm, "qAlloc"):
        q = [qvm.qAlloc(), qvm.qAlloc()]
    elif hasattr(qvm, "qalloc"):
        q = [qvm.qalloc(), qvm.qalloc()]
    else:
        q = [qvm.allocate_qubit(), qvm.allocate_qubit()]

    prog = QProg()
    prog << X(q[0])
    prog << X(q[1])

    create_operator._qvm = qvm
    create_operator._qubits = q
    return prog
