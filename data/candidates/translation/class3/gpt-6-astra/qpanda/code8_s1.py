# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq


def rx_gate(value=None):
    circuit = pq.QCircuit()
    if value is not None:
        circuit << pq.RX(0, float(value))
        return circuit

    for name in ("Parameter", "QParameter", "Param"):
        parameter_type = getattr(pq, name, None)
        if parameter_type is None:
            continue
        try:
            theta = parameter_type("theta")
            gate = pq.RX(0, theta)
        except (TypeError, ValueError):
            continue
        circuit << gate
        return circuit

    circuit << pq.RX(0, "theta")
    return circuit
