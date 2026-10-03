# EVAL_META: task_id=77, framework=qpanda, class=1
import math

from pyqpanda3.core import QProg, RY, CNOT


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        math.sqrt(probability_dist.get(state, 0))
        for state in range(1 << num_qubits)
    ]
    weights = [amplitude * amplitude for amplitude in amplitudes]
    norm = math.sqrt(sum(weights))
    if not math.isclose(norm, 1.0, abs_tol=1e-10):
        raise ValueError("The state amplitudes must have unit norm.")

    program = QProg()

    for target in range(num_qubits - 1, -1, -1):
        half_block = 1 << target
        block_size = half_block << 1
        control_count = num_qubits - target - 1
        rotation_count = 1 << control_count

        angles = []
        for prefix in range(rotation_count):
            start = prefix * block_size
            zero_weight = sum(weights[start:start + half_block])
            one_weight = sum(weights[start + half_block:start + block_size])
            angles.append(
                2.0 * math.atan2(math.sqrt(one_weight), math.sqrt(zero_weight))
            )

        stride = 1
        while stride < rotation_count:
            for start in range(0, rotation_count, stride << 1):
                for offset in range(stride):
                    left = start + offset
                    right = left + stride
                    a, b = angles[left], angles[right]
                    angles[left] = a + b
                    angles[right] = a - b
            stride <<= 1

        for index in range(rotation_count):
            gray = index ^ (index >> 1)
            program << RY(target, angles[gray] / rotation_count)

            if control_count:
                next_index = (index + 1) % rotation_count
                next_gray = next_index ^ (next_index >> 1)
                changed_bit = (gray ^ next_gray).bit_length() - 1
                program << CNOT(target + 1 + changed_bit, target)

    return program
