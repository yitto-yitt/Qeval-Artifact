# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import pyqpanda as pq


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    dim = 1 << num_qubits
    probabilities = [float(probability_dist.get(i, 0.0)) for i in range(dim)]

    try:
        qubits = pq.qAlloc_many(num_qubits)
    except Exception:
        pq.init(pq.QMachineType.CPU)
        qubits = pq.qAlloc_many(num_qubits)

    circuit = pq.QCircuit()

    for target in range(num_qubits - 1, -1, -1):
        high_count = num_qubits - target - 1
        for prefix in range(1 << high_count):
            p0 = 0.0
            p1 = 0.0
            for low in range(1 << target):
                p0 += probabilities[(prefix << (target + 1)) | low]
                p1 += probabilities[(prefix << (target + 1)) | (1 << target) | low]

            total = p0 + p1
            if total <= 0.0:
                continue

            theta = 2.0 * math.atan2(math.sqrt(max(p1, 0.0)), math.sqrt(max(p0, 0.0)))

            controls = []
            zero_controls = []
            for q_index in range(target + 1, num_qubits):
                bit = (prefix >> (q_index - target - 1)) & 1
                controls.append(qubits[q_index])
                if bit == 0:
                    zero_controls.append(qubits[q_index])

            for q in zero_controls:
                circuit << pq.X(q)

            gate = pq.RY(qubits[target], theta)
            if controls:
                gate = gate.control(controls)
            circuit << gate

            for q in zero_controls:
                circuit << pq.X(q)

    return circuit
