# EVAL_META: task_id=77, framework=pennylane, class=1
import math
import pennylane as qml

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    with qml.tape.QuantumTape() as tape:
        qml.StatePrep(amplitudes, wires=list(range(num_qubits)))
        
    return tape
