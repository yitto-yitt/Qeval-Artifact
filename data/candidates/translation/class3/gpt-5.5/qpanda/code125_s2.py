# EVAL_META: task_id=125, framework=qpanda, class=3
import pyqpanda3.core as pq


def circ_to_gate(circ):
    for name in ("to_gate", "to_qgate", "to_QGate", "to_gate_node"):
        attr = getattr(circ, name, None)
        if attr is not None:
            if callable(attr):
                try:
                    return attr()
                except TypeError:
                    pass
            else:
                return attr

    for name in (
        "circuit_to_gate",
        "convert_circuit_to_gate",
        "qcircuit_to_qgate",
        "convert_qcircuit_to_qgate",
        "QCircuitToQGate",
        "circuitToGate",
    ):
        func = getattr(pq, name, None)
        if callable(func):
            try:
                return func(circ)
            except TypeError:
                pass

    qgate_cls = getattr(pq, "QGate", None)
    if qgate_cls is not None:
        try:
            return qgate_cls(circ)
        except Exception:
            pass

    return circ
