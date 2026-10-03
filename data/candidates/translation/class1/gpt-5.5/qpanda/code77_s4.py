# EVAL_META: task_id=77, framework=qpanda, class=1
import math
from pyqpanda3.core import *


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [math.sqrt(probability_dist.get(basis_state, 0)) for basis_state in range(2 ** num_qubits)]

    def _new_circuit():
        try:
            return QCircuit()
        except TypeError:
            return QCircuit(num_qubits)

    machine = None
    try:
        machine = CPUQVM()
        for init_name in ("init_qvm", "init", "initQVM"):
            if hasattr(machine, init_name):
                try:
                    getattr(machine, init_name)()
                except TypeError:
                    pass
                break
        allocator = getattr(machine, "qAlloc_many", None) or getattr(machine, "qalloc_many", None)
        qubits = allocator(num_qubits)
    except Exception:
        machine = None
        qubits = list(range(num_qubits))

    if machine is not None:
        if not hasattr(circuit_from_probability_dist, "_keepalive"):
            circuit_from_probability_dist._keepalive = []
        circuit_from_probability_dist._keepalive.append((machine, qubits))

    circuit = _new_circuit()

    encoder = globals().get("amplitude_encode")
    if encoder is not None:
        try:
            encoded = encoder(qubits, amplitudes)
            try:
                circuit << encoded
                return circuit
            except Exception:
                return encoded
        except Exception:
            pass

    probs = [amp * amp for amp in amplitudes]

    def _apply_controlled_ry(target, controls, pattern, angle):
        if abs(angle) < 1e-15:
            return

        flipped = []
        for control_index, bit in zip(controls, pattern):
            if bit == 0:
                circuit << X(qubits[control_index])
                flipped.append(control_index)

        gate = RY(qubits[target], angle)
        if controls:
            control_qubits = [qubits[i] for i in controls]
            controlled_gate = gate.control(control_qubits)
            if controlled_gate is not None:
                gate = controlled_gate
        circuit << gate

        for control_index in reversed(flipped):
            circuit << X(qubits[control_index])

    for target in range(num_qubits - 1, -1, -1):
        block_size = 1 << (target + 1)
        half_block = 1 << target
        controls = list(range(target + 1, num_qubits))

        for prefix in range(1 << (num_qubits - target - 1)):
            start = prefix * block_size
            p0 = sum(probs[start:start + half_block])
            p1 = sum(probs[start + half_block:start + block_size])

            if p0 == 0 and p1 == 0:
                angle = 0.0
            else:
                angle = 2.0 * math.atan2(math.sqrt(p1), math.sqrt(p0))

            pattern = [(prefix >> (control - target - 1)) & 1 for control in controls]
            _apply_controlled_ry(target, controls, pattern, angle)

    return circuit
