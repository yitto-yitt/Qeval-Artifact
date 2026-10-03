# EVAL_META: task_id=78, framework=qpanda, class=3
import math
from pyqpanda3.core import *

def qft_no_swaps(num_qubits):
    def _append(circuit, op):
        try:
            result = circuit << op
            return circuit if result is None else result
        except Exception:
            result = circuit.insert(op)
            return circuit if result is None else result

    def _make_circuit():
        try:
            return QCircuit()
        except TypeError:
            return QCircuit(num_qubits)

    def _controlled_phase(circuit, control, target, angle):
        for gate_name in ("CR", "CPHASE", "CP"):
            gate_factory = globals().get(gate_name)
            if gate_factory is not None:
                for args in ((control, target, angle), (angle, control, target)):
                    try:
                        return _append(circuit, gate_factory(*args))
                    except Exception:
                        pass

        phase_factory = globals().get("U1", None)
        if phase_factory is not None:
            circuit = _append(circuit, phase_factory(control, angle / 2.0))
            circuit = _append(circuit, phase_factory(target, angle / 2.0))
            circuit = _append(circuit, CNOT(control, target))
            circuit = _append(circuit, phase_factory(target, -angle / 2.0))
            circuit = _append(circuit, CNOT(control, target))
            return circuit

        circuit = _append(circuit, RZ(control, angle / 2.0))
        circuit = _append(circuit, RZ(target, angle / 2.0))
        circuit = _append(circuit, CNOT(control, target))
        circuit = _append(circuit, RZ(target, -angle / 2.0))
        circuit = _append(circuit, CNOT(control, target))
        return circuit

    circuit = _make_circuit()
    qubits = list(range(num_qubits))

    for j in range(num_qubits):
        for k in range(j):
            angle = -math.pi / (2 ** (j - k))
            circuit = _controlled_phase(circuit, qubits[j], qubits[k], angle)
        circuit = _append(circuit, H(qubits[j]))

    return circuit
