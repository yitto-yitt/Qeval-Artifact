# EVAL_META: task_id=77, framework=cirq, class=1
import math
import cirq


def circuit_from_probability_dist(probability_dist):
    if probability_dist:
        max_key = max(probability_dist.keys())
    else:
        max_key = 0
    num_qubits = math.ceil(math.log2(max_key + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(amplitudes)(*qubits))
    return circuit
