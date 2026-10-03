# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import *

def inv_circuit(n):
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(n)
    elif hasattr(qvm, "qalloc_many"):
        q = qvm.qalloc_many(n)
    elif hasattr(qvm, "qAllocMany"):
        q = qvm.qAllocMany(n)
    else:
        q = list(range(n))

    def add_gate(circuit, gate):
        if hasattr(circuit, "insert"):
            ret = circuit.insert(gate)
        else:
            ret = circuit << gate
        return circuit if ret is None else ret

    qc = QCircuit()
    for i in range(2):
        qc = add_gate(qc, H(q[i + 1]))
    for i in range(2):
        qc = add_gate(qc, CNOT(q[i + 1], q[i + 3]))

    try:
        inv = qc.dagger()
        if inv is not None and not isinstance(inv, bool):
            if not hasattr(inv_circuit, "_qvms"):
                inv_circuit._qvms = []
            inv_circuit._qvms.append(qvm)
            return inv
    except Exception:
        pass

    try:
        ret = qc.set_dagger(True)
        inv = qc if ret is None or isinstance(ret, bool) else ret
        if not hasattr(inv_circuit, "_qvms"):
            inv_circuit._qvms = []
        inv_circuit._qvms.append(qvm)
        return inv
    except Exception:
        pass

    inv = QCircuit()
    inv = add_gate(inv, CNOT(q[2], q[4]))
    inv = add_gate(inv, CNOT(q[1], q[3]))
    inv = add_gate(inv, H(q[2]))
    inv = add_gate(inv, H(q[1]))

    if not hasattr(inv_circuit, "_qvms"):
        inv_circuit._qvms = []
    inv_circuit._qvms.append(qvm)
    return inv
