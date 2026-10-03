# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq

def rx_gate(value=None):
    if value is None:
        parameter_type = getattr(pq, "Parameter", None)
        theta = parameter_type("theta") if parameter_type is not None else "theta"
    else:
        theta = float(value)

    program = pq.QProg()
    program << pq.RX(0, theta)
    return program
