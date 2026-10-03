# EVAL_META: task_id=77, framework=qpanda2, class=1
import math

from pyqpanda import CPUQVM, QCircuit, QProg, RY, X


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        math.sqrt(probability_dist.get(state, 0))
        for state in range(2**num_qubits)
    ]
    norm = math.sqrt(math.fsum(a * a for a in amplitudes))
    if not math.isclose(norm, 1.0, rel_tol=1e-10, abs_tol=1e-10):
        raise ValueError("State amplitudes must have unit norm.")

    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    circuit = QCircuit()

    for target in range(num_qubits - 1, -1, -1):
        block_size = 1 << (target + 1)
        half_size = 1 << target
        for prefix in range(1 << (num_qubits - target - 1)):
            start = prefix * block_size
            weight_zero = math.fsum(
                amplitudes[i] ** 2
                for i in range(start, start + half_size)
            )
            weight_one = math.fsum(
                amplitudes[i] ** 2
                for i in range(start + half_size, start + block_size)
            )
            if weight_zero + weight_one == 0:
                continue

            angle = 2 * math.atan2(
                math.sqrt(weight_one), math.sqrt(weight_zero)
            )
            controls = qubits[target + 1:]
            negative_controls = [
                qubit
                for bit, qubit in enumerate(controls)
                if not ((prefix >> bit) & 1)
            ]

            for qubit in negative_controls:
                circuit << X(qubit)

            rotation = RY(qubits[target], angle)
            if controls:
                rotation = rotation.control(controls)
            circuit << rotation

            for qubit in reversed(negative_controls):
                circuit << X(qubit)

    program = QProg()
    program << circuit
    machine.directly_run(program)

    if not hasattr(circuit_from_probability_dist, "_machines"):
        circuit_from_probability_dist._machines = []
    circuit_from_probability_dist._machines.append(machine)
    return circuit
