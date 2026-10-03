# EVAL_META: task_id=77, framework=qpanda, class=1
import math
from pyqpanda3.core import QProg, RY, CNOT


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        math.sqrt(probability_dist.get(basis_state, 0))
        for basis_state in range(2**num_qubits)
    ]
    weights = [amplitude * amplitude for amplitude in amplitudes]
    program = QProg()

    for target in range(num_qubits - 1, -1, -1):
        block_size = 1 << target
        num_controls = num_qubits - target - 1
        num_angles = 1 << num_controls
        angles = []

        for prefix in range(num_angles):
            start = prefix * 2 * block_size
            weight_zero = sum(weights[start:start + block_size])
            weight_one = sum(
                weights[start + block_size:start + 2 * block_size]
            )
            angles.append(
                2 * math.atan2(math.sqrt(weight_one), math.sqrt(weight_zero))
            )

        stride = 1
        while stride < num_angles:
            for start in range(0, num_angles, 2 * stride):
                for offset in range(stride):
                    left = start + offset
                    right = left + stride
                    a, b = angles[left], angles[right]
                    angles[left] = a + b
                    angles[right] = a - b
            stride *= 2

        for index in range(num_angles):
            gray = index ^ (index >> 1)
            program << RY(target, angles[gray] / num_angles)

            if num_controls:
                next_index = (index + 1) % num_angles
                next_gray = next_index ^ (next_index >> 1)
                changed_bit = (gray ^ next_gray).bit_length() - 1
                program << CNOT(target + 1 + changed_bit, target)

    return program
