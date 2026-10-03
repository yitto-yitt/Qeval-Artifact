# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1, shots=samples)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.counts(wires=0)
    
    counts = circuit()
    total = sum(counts.values())
    
    heads = counts.get('0', 0) + counts.get(0, 0)
    tails = counts.get('1', 0) + counts.get(1, 0)
    
    return {'Heads': heads / total, 'Tails': tails / total}
