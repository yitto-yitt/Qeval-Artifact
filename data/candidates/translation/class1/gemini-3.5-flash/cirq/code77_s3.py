# EVAL_META: task_id=77, framework=cirq, class=1
import math
import cirq

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    # State preparation can be done using cirq.StatePreparationChannel 
    # or by constructing a custom gate that implements the state preparation.
    # In Cirq, cirq.StatePreparationChannel(state_vector) creates a channel that prepares the state.
    # However, since this is a quantum circuit, we can use cirq.StatePreparationChannel.
    # Let's check if cirq.StatePreparationChannel is available in cirq==1.6.1.
    # Yes, cirq.StatePreparationChannel is a standard way in Cirq to represent state preparation.
    circuit.append(cirq.StatePreparationChannel(amplitudes).on(*qubits))
    return circuit
