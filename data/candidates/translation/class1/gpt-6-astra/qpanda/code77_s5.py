# EVAL_META: task_id=77, framework=qpanda, class=1
import math

from pyqpanda3.core import QProg, RY, CNOT


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        math.sqrt(probability_dist.get(basis_state, 0))
        for basis_state in range(2**num_qubits)
    ]
    norm = math.sqrt(math.fsum(amplitude**2 for amplitude in amplitudes))
    if not math.isclose(norm, 1.0, rel_tol=1e-5, abs_tol=1e-10):
        raise ValueError("State amplitudes must be normalized.")

    probabilities = [amplitude**2 for amplitude in amplitudes]
    program = QProg()

    for target in range(num_qubits - 1, -1, -1):
        num_controls = num_qubits - target - 1
        count = 1 << num_controls
        half_block = 1 << target
        angles = []

        for prefix in range(count):
            start = prefix << (target + 1)
            left = math.fsum(probabilities[start:start + half_block])
            right = math.fsum(
                probabilities[start + half_block:start + 2 * half_block]
            )
            angles.append(2 * math.atan2(math.sqrt(right), math.sqrt(left)))

        if num_controls == 0:
            program << RY(target, angles[0])
            continue

        gray_codes = [index ^ (index >> 1) for index in range(count)]
        for index, gray in enumerate(gray_codes):
            angle = math.fsum(
                (-1 if bin(prefix & gray).count("1") % 2 else 1)
                * angles[prefix]
                for prefix in range(count)
            ) / count
            program << RY(target, angle)

            next_gray = gray_codes[(index + 1) % count]
            changed_bit = (gray ^ next_gray).bit_length() - 1
            program << CNOT(target + 1 + changed_bit, target)

    return program
