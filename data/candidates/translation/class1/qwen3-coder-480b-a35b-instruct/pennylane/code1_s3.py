# EVAL_META: task_id=1, framework=pennylane, class=1
import pennylane as qml

def run_bell_state_simulator():
    dev = qml.device("default.qubit", wires=2, shots=1000)
    
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(qml.PauliZ(wires=0)), qml.sample(qml.PauliZ(wires=1))
    
    samples = bell_circuit()
    # Convert Z-basis samples to bitstrings
    bitstrings = []
    for i in range(samples[0].shape[0]):
        bit0 = '0' if samples[0][i] == 1 else '1'
        bit1 = '0' if samples[1][i] == 1 else '1'
        bitstrings.append(bit0 + bit1)
    
    # Count occurrences of each bitstring
    counts = {}
    for bitstring in bitstrings:
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Normalize to get probabilities
    total = len(bitstrings)
    return {key: value / total for key, value in counts.items()}
