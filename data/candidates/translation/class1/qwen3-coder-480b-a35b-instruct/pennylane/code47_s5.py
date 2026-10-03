# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1, shots=samples)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(qml.PauliZ(wires=0))
    
    results = circuit()
    
    # Count the number of +1 (corresponding to |0>) and -1 (corresponding to |1>)
    heads_count = sum(1 for r in results if r == 1)  # |0> state -> Heads
    tails_count = sum(1 for r in results if r == -1)  # |1> state -> Tails
    
    total = len(results)
    return {
        'Heads': heads_count / total,
        'Tails': tails_count / total
    }
