# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import *

def mcy(qc):
    container = qc
    qubits = None

    if isinstance(qc, dict):
        container = qc.get("qc", qc.get("circuit", qc.get("prog", qc.get("program", qc))))
        qubits = qc.get("qubits", qc.get("qbits", qc.get("qvec", qc.get("qlist", None))))
    elif isinstance(qc, (tuple, list)) and len(qc) >= 2:
        try:
            if len(qc[1]) >= 5:
                container = qc[0]
                qubits = qc[1]
        except Exception:
            pass

    if qubits is None:
        for name in ("qubits", "qbits", "qvec", "qlist", "qv"):
            if hasattr(container, name):
                qubits = getattr(container, name)
                if callable(qubits):
                    qubits = qubits()
                break

    if qubits is None:
        for name in ("get_qubits", "get_qbits", "get_qvec", "get_used_qubits"):
            if hasattr(container, name):
                try:
                    qubits = getattr(container, name)()
                    break
                except Exception:
                    pass

    if qubits is None:
        qubits = list(range(5))

    controls = [qubits[i] for i in range(4)]
    target = qubits[4]

    gate = Y(target)

    controlled = False
    for name in ("control", "set_control", "setControl"):
        if hasattr(gate, name):
            method = getattr(gate, name)
            try:
                result = method(controls)
            except TypeError:
                result = method(*controls)
            if result is not None:
                gate = result
            controlled = True
            break

    if not controlled:
        raise AttributeError("Controlled gate operation is not supported by this pyQPanda3 gate object.")

    try:
        result = container << gate
        if result is not None and not isinstance(qc, (tuple, list, dict)):
            return result
    except Exception:
        if hasattr(container, "insert"):
            result = container.insert(gate)
            if result is not None and not isinstance(qc, (tuple, list, dict)):
                return result
        elif hasattr(container, "append"):
            container.append(gate)
        else:
            raise

    return qc
