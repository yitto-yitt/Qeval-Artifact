# EVAL_META: task_id=77, framework=qpanda2, class=1
import math

from pyqpanda import QuantumCircuit, init, QMachineType


def circuit_from_probability_dist(probability_dist):
    init(QMachineType.CPU)
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        math.sqrt(probability_dist.get(basis_state, 0.0))
        for basis_state in range(2 ** num_qubits)
    ]
    qc = QuantumCircuit(num_qubits)
    qc.initialize(amplitudes, list(range(num_qubits)))
    return qc
