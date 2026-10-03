# EVAL_META: task_id=109, framework=qpanda, class=3
import pyqpanda3.core as pq


def circuit():
    try:
        rotation = pq.RZ(0, "th")
    except (TypeError, ValueError):
        rotation = None
        for name in ("Parameter", "QParameter", "Param", "Var", "var"):
            parameter_type = getattr(pq, name, None)
            if parameter_type is None:
                continue
            try:
                theta = parameter_type("th")
                rotation = pq.RZ(0, theta)
                break
            except (TypeError, ValueError):
                continue
        if rotation is None:
            raise RuntimeError("The framework does not expose a symbolic RZ parameter.")

    program = pq.QProg()
    program << pq.H(0)
    program << rotation
    return program
