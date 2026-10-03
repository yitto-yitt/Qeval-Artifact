# EVAL_META: task_id=77, framework=qpanda, class=1
import math

from pyqpanda3.core import CNOT, QProg, RY


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        math.sqrt(probability_dist.get(state, 0))
        for state in range(2**num_qubits)
    ]

    circuit = QProg()

    for target in range(num_qubits - 1, -1, -1):
        num_controls = num_qubits - target - 1
        num_angles = 1 << num_controls
        half_block = 1 << target
        angles = []

        for prefix in range(num_angles):
            start = prefix << (target + 1)
            left = math.fsum(
                amplitude * amplitude
                for amplitude in amplitudes[start:start + half_block]
            )
            right = math.fsum(
                amplitude * amplitude
                for amplitude in amplitudes[
                    start + half_block:start + 2 * half_block
                ]
            )
            angles.append(2 * math.atan2(math.sqrt(right), math.sqrt(left)))

        stride = 1
        while stride < num_angles:
            for start in range(0, num_angles, 2 * stride):
                for offset in range(stride):
                    i = start + offset
                    j = i + stride
                    left, right = angles[i], angles[j]
                    angles[i] = left + right
                    angles[j] = left - right
            stride *= 2

        for index in range(num_angles):
            gray = index ^ (index >> 1)
            circuit << RY(target, angles[gray] / num_angles)

            if num_controls:
                next_index = (index + 1) % num_angles
                next_gray = next_index ^ (next_index >> 1)
                changed_bit = (gray ^ next_gray).bit_length() - 1
                circuit << CNOT(target + 1 + changed_bit, target)

    return circuit
