# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import pyqpanda as pq


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    try:
        pq.init_quantum_machine(pq.QMachineType.CPU)
    except Exception:
        pass

    qubits = pq.qAlloc_many(num_qubits)

    if hasattr(pq, "AmplitudeEncode"):
        circuit = pq.AmplitudeEncode(qubits, amplitudes)
    elif hasattr(pq, "amplitude_encode"):
        circuit = pq.amplitude_encode(qubits, amplitudes)
    else:
        raise AttributeError(
            "pyqpanda has no AmplitudeEncode or amplitude_encode"
        )

    return circuit
