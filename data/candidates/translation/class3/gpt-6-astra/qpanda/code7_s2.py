# EVAL_META: task_id=7, framework=qpanda, class=3
import pyqpanda3.core as pq


def create_parametrized_gate():
    parameter_types = ("Parameter", "QParameter", "QParam", "Symbol")
    for name in parameter_types:
        parameter_type = getattr(pq, name, None)
        if parameter_type is None:
            continue
        try:
            theta = parameter_type("theta")
            gate = pq.RX(0, theta)
        except (TypeError, ValueError, RuntimeError):
            continue
        circuit = pq.QProg()
        circuit << gate
        return circuit

    try:
        gate = pq.RX(0, "theta")
    except (TypeError, ValueError, RuntimeError):
        from sympy import Symbol
        gate = pq.RX(0, Symbol("theta"))

    circuit = pq.QProg()
    circuit << gate
    return circuit
