# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import pyqpanda as pq

_QVM = None


def _get_qvm():
    global _QVM
    if _QVM is None:
        _QVM = pq.CPUQVM()
        _QVM.init_qvm()
    return _QVM


def _insert_controlled_ry(circuit, qubits, target, control_bits, control_values, angle):
    if abs(angle) < 1e-15:
        return

    flipped = []
    for bit, value in zip(control_bits, control_values):
        if value == 0:
            circuit.insert(pq.X(qubits[bit]))
            flipped.append(bit)

    gate = pq.RY(qubits[target], angle)
    if control_bits:
        gate = gate.control([qubits[bit] for bit in control_bits])
    circuit.insert(gate)

    for bit in reversed(flipped):
        circuit.insert(pq.X(qubits[bit]))


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    probs = [float(probability_dist.get(basis_state, 0)) for basis_state in range(2 ** num_qubits)]

    qvm = _get_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    circuit = pq.QCircuit()

    for target in range(num_qubits - 1, -1, -1):
        control_bits = list(range(num_qubits - 1, target, -1))
        num_controls = len(control_bits)

        for assignment in range(2 ** num_controls):
            control_values = [
                (assignment >> (num_controls - 1 - i)) & 1
                for i in range(num_controls)
            ]

            prob_zero = 0.0
            prob_one = 0.0

            for basis_state, prob in enumerate(probs):
                matches_controls = True
                for bit, value in zip(control_bits, control_values):
                    if ((basis_state >> bit) & 1) != value:
                        matches_controls = False
                        break

                if matches_controls:
                    if ((basis_state >> target) & 1) == 0:
                        prob_zero += prob
                    else:
                        prob_one += prob

            if prob_zero == 0.0 and prob_one == 0.0:
                angle = 0.0
            else:
                angle = 2.0 * math.atan2(math.sqrt(prob_one), math.sqrt(prob_zero))

            _insert_controlled_ry(circuit, qubits, target, control_bits, control_values, angle)

    return circuit
