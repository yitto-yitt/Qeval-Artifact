# EVAL_META: task_id=77, framework=qpanda, class=1
import math
from pyqpanda3.core import QProg, RY, X


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        math.sqrt(probability_dist.get(basis_state, 0))
        for basis_state in range(2**num_qubits)
    ]
    weights = [amplitude * amplitude for amplitude in amplitudes]
    norm = math.sqrt(math.fsum(weights))
    if not math.isclose(norm, 1.0, abs_tol=1e-10):
        raise ValueError("State amplitudes must have unit norm.")

    prog = QProg()
    for target in range(num_qubits - 1, -1, -1):
        controls = list(range(target + 1, num_qubits))
        half = 1 << target

        for prefix in range(1 << len(controls)):
            start = prefix << (target + 1)
            mass_zero = math.fsum(weights[start:start + half])
            mass_one = math.fsum(weights[start + half:start + 2 * half])
            if mass_zero + mass_one == 0:
                continue

            angle = 2 * math.atan2(math.sqrt(mass_one), math.sqrt(mass_zero))
            zero_controls = [
                qubit
                for qubit in controls
                if not (prefix & (1 << (qubit - target - 1)))
            ]

            for qubit in zero_controls:
                prog << X(qubit)

            gate = RY(target, angle)
            if controls:
                gate = gate.control(controls)
            prog << gate

            for qubit in reversed(zero_controls):
                prog << X(qubit)

    return prog
