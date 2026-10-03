# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1, shots=samples)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(qml.PauliZ(0))
    
    results = circuit()
    
    # Convert PauliZ eigenvalues to bit outcomes
    # -1 (Tails) and +1 (Heads)
    if samples == 1:
        results = [results]
    
    counts = Counter(results)
    total = len(results)
    
    # Map PauliZ outcomes to Heads/Tails
    heads_count = counts.get(1, 0)  # +1 -> Heads
    tails_count = counts.get(-1, 0) # -1 -> Tails
    
    return {'Heads': heads_count / total, 'Tails': tails_count / total}
