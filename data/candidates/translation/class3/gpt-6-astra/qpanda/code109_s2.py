# EVAL_META: task_id=109, framework=qpanda, class=3
import pyqpanda3.core as pq


def circuit():
    parameters = []
    for name in ("Parameter", "QParameter", "QParam"):
        parameter_type = getattr(pq, name, None)
        if parameter_type is not None:
            try:
                parameters.append(parameter_type("th"))
            except (TypeError, ValueError, RuntimeError):
                pass
    parameters.append("th")

    for theta in parameters:
        try:
            rotation = pq.RZ(0, theta)
            program = pq.QProg()
            program << pq.H(0) << rotation
            return program
        except (TypeError, ValueError, RuntimeError):
            continue

    raise RuntimeError("The framework does not expose a supported symbolic RZ parameter.")
