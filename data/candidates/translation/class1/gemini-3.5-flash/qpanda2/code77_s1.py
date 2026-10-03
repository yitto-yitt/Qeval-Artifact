# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import pyqpanda as pq

_global_machine = None


def circuit_from_probability_dist(probability_dist):
    global _global_machine
    if _global_machine is None:
        _global_machine = pq.CPUQVM()
        _global_machine.init_qvm()

    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    _global_machine.qFree_all()
    qubits = _global_machine.qAlloc_many(num_qubits)

    circuit = pq.amplitude_encode(qubits, amplitudes)
    return circuit
