# EVAL_META: task_id=77, framework=pennylane, class=1
import math
import pennylane as qml


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    dev = qml.device('default.qubit', wires=num_qubits)
    
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(amplitudes, wires=range(num_qubits))
        return qml.probs(wires=range(num_qubits))
    
    # We need to return the operation that prepares the state
    def state_prep_circuit():
        qml.StatePrep(amplitudes, wires=range(num_qubits))
        
    return state_prep_circuit
