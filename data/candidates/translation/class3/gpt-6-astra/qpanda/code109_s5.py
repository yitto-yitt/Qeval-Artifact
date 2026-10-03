# EVAL_META: task_id=109, framework=qpanda, class=3
import pyqpanda3.core as pq


def circuit():
    rotation = None
    for name in ("Parameter", "QParameter", "Param"):
        parameter_type = getattr(pq, name, None)
        if parameter_type is not None:
            try:
                rotation = pq.RZ(0, parameter_type("th"))
                break
            except (TypeError, ValueError):
                continue

    if rotation is None:
        rotation = pq.RZ(0, "th")

    program = pq.QProg()
    program << pq.H(0)
    program << rotation
    return program
