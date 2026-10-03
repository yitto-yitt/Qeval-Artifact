# EVAL_META: task_id=109, framework=qpanda, class=3
import pyqpanda3.core as pq


def circuit():
    for name in ("Parameter", "QParameter", "QParam", "Param"):
        parameter_type = getattr(pq, name, None)
        if parameter_type is None:
            continue
        try:
            theta = parameter_type("th")
            rotation = pq.RZ(0, theta)
        except (TypeError, ValueError):
            continue
        program = pq.QProg()
        program << pq.H(0) << rotation
        return program

    program = pq.QProg()
    program << pq.H(0) << pq.RZ(0, "th")
    return program
