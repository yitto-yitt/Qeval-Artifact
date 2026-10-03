# EVAL_META: task_id=147, framework=pennylane, class=3
import pennylane as qml

def mcy(qc):
    try:
        active = qml.queuing.QueuingManager.active_context()
    except Exception:
        active = None

    with qml.queuing.QueuingManager.stop_recording():
        op = qml.ctrl(qml.PauliY(wires=4), control=[0, 1, 2, 3])

    if active is qc:
        qml.apply(op)
    elif hasattr(qc, "_ops"):
        qc._ops.append(op)
    elif hasattr(qc, "append"):
        qc.append(op)
    else:
        qml.apply(op)

    return qc
