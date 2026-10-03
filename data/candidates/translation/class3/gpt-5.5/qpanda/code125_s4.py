# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import *


def circ_to_gate(circ):
    for name in (
        "to_gate",
        "toGate",
        "to_qgate",
        "toQGate",
        "convert_to_gate",
        "convert_to_qgate",
    ):
        attr = getattr(circ, name, None)
        if attr is not None:
            try:
                return attr() if callable(attr) else attr
            except TypeError:
                pass

    for name in (
        "circuit_to_gate",
        "circuitToGate",
        "QCircuitToQGate",
        "qCircuitToQGate",
        "qcircuit_to_gate",
        "qcircuit_to_qgate",
        "convert_circuit_to_gate",
        "convert_qcircuit_to_qgate",
    ):
        func = globals().get(name)
        if callable(func):
            try:
                return func(circ)
            except TypeError:
                pass

    return circ
