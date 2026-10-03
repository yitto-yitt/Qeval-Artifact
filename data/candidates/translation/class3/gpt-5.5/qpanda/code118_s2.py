# EVAL_META: task_id=118, framework=qpanda, class=3
import math
from pyqpanda3.core import *

def create_c3sx_circuit():
    circuit = QCircuit()

    def _append_controlled(gate, ctrls):
        controlled_gate = gate
        result = controlled_gate.control(ctrls)
        if result is not None:
            controlled_gate = result
        circuit << controlled_gate

    try:
        _append_controlled(SX(3), [0, 1, 2])
    except Exception:
        phase_gate = P(2, math.pi / 4)
        phase_result = phase_gate.control([0, 1])
        if phase_result is not None:
            phase_gate = phase_result
        circuit << phase_gate

        rx_gate = RX(3, math.pi / 2)
        rx_result = rx_gate.control([0, 1, 2])
        if rx_result is not None:
            rx_gate = rx_result
        circuit << rx_gate

    return circuit
