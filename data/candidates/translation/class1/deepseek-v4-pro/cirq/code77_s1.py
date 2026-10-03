# EVAL_META: task_id=77, framework=cirq, class=1
import math
import cirq

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    state_vector = [0.0] * (2 ** num_qubits)
    for basis_state in range(2 ** num_qubits):
        prob = probability_dist.get(basis_state, 0)
        state_vector[basis_state] = math.sqrt(prob)
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(state_vector).on(*qubits))
    return circuit
