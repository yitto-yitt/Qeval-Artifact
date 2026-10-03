# EVAL_META: task_id=109, framework=qpanda, class=3
import pyqpanda3.core as pq


def circuit():
    parameters = []
    for name in ("Parameter", "QParameter", "QParam", "Symbol"):
        factory = getattr(pq, name, None)
        if factory is not None:
            try:
                parameters.append(factory("th"))
            except (TypeError, ValueError, RuntimeError):
                pass
    parameters.append("th")

    last_error = None
    for theta in parameters:
        try:
            rotation = pq.RZ(0, theta)
            prog = pq.QProg()
            prog << pq.H(0) << rotation
            return prog
        except (TypeError, ValueError, RuntimeError) as error:
            last_error = error

    raise RuntimeError("The core API does not expose a symbolic RZ parameter.") from last_error
