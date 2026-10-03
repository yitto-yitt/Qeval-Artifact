# EVAL_META: task_id=7, framework=qpanda, class=3
import pyqpanda3.core as pq


def create_parametrized_gate():
    for name in ("Parameter", "Param", "QParameter", "QParam", "ParameterExpression"):
        parameter_type = getattr(pq, name, None)
        if parameter_type is None:
            continue
        try:
            theta = parameter_type("theta")
            gate = pq.RX(0, theta)
        except (TypeError, ValueError, RuntimeError):
            continue
        program = pq.QProg()
        program << gate
        return program

    program = pq.QProg()
    program << pq.RX(0, "theta")
    return program
