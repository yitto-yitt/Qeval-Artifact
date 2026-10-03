# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import *

def mcy(qc):
    controls = [0, 1, 2, 3]
    target = 4

    for name in ("qubits", "qbits", "qv", "qubit_list", "get_qubits", "get_used_qubits"):
        try:
            qv = getattr(qc, name)
            if callable(qv):
                qv = qv()
            if len(qv) >= 5:
                controls = [qv[0], qv[1], qv[2], qv[3]]
                target = qv[4]
                break
        except Exception:
            pass

    gate = Y(target)
    try:
        controlled_gate = gate.control(controls)
        if controlled_gate is not None:
            gate = controlled_gate
    except Exception:
        gate.set_control(controls)

    try:
        result = qc << gate
        if result is not None:
            qc = result
    except Exception:
        result = qc.insert(gate)
        if result is not None:
            qc = result

    return qc
