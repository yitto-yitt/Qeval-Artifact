# EVAL_META: task_id=78, framework=qpanda, class=3
import math
from pyqpanda3.core import *

def qft_no_swaps(num_qubits):
    try:
        circuit = QCircuit(num_qubits)
    except Exception:
        circuit = QCircuit()

    def _append(gate):
        nonlocal circuit
        try:
            result = circuit << gate
            if result is not None:
                circuit = result
        except Exception:
            result = circuit.insert(gate)
            if result is not None:
                circuit = result

    def _phase(qubit, angle):
        try:
            return P(qubit, angle)
        except Exception:
            try:
                return U1(qubit, angle)
            except Exception:
                return RZ(qubit, angle)

    def _cnot(control, target):
        try:
            return CNOT(control, target)
        except Exception:
            return CX(control, target)

    def _controlled_phase(control, target, angle):
        half = angle / 2.0
        _append(_phase(control, half))
        _append(_phase(target, half))
        _append(_cnot(control, target))
        _append(_phase(target, -half))
        _append(_cnot(control, target))

    for target in range(num_qubits):
        for control in range(target):
            _controlled_phase(control, target, -math.pi / (2 ** (target - control)))
        _append(H(target))

    return circuit
