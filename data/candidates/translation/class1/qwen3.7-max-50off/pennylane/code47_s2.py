# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1, shots=samples)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.counts()
    
    counts = circuit()
    total = sum(counts.values())
    
    heads = 0
    tails = 0
    for k, v in counts.items():
        if str(k) == '0':
            heads = v
        elif str(k) == '1':
            tails = v
            
    return {'Heads': heads / total, 'Tails': tails / total}
