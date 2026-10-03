# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device('default.qubit', wires=1, shots=samples)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.counts()
        
    counts = circuit()
    total = sum(counts.values())
    
    heads_count = counts.get(0, 0) + counts.get('0', 0)
    tails_count = counts.get(1, 0) + counts.get('1', 0)
    
    return {'Heads': heads_count / total, 'Tails': tails_count / total}
