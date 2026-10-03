# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml

def bell_each_shot():
    dev = qml.device("default.qubit", wires=2, shots=10)
    
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(qml.PauliZ(wires=0)), qml.sample(qml.PauliZ(wires=1))
    
    results = bell_circuit()
    
    # Convert Z-basis samples to bitstrings
    bitstrings = []
    for i in range(len(results[0])):
        bit0 = '0' if results[0][i] == 1 else '1'
        bit1 = '0' if results[1][i] == 1 else '1'
        bitstrings.append(bit0 + bit1)
    
    # Count occurrences of each bitstring
    counts = {}
    for bitstring in bitstrings:
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Convert counts to probabilities
    total_shots = len(bitstrings)
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    
    return prob_dist
