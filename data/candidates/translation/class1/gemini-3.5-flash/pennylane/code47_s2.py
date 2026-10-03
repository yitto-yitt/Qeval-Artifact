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
    
    count_0 = 0
    count_1 = 0
    for k, v in counts.items():
        if str(k) == '0' or k == 0:
            count_0 += v
        elif str(k) == '1' or k == 1:
            count_1 += v
            
    return {'Heads': count_0 / total, 'Tails': count_1 / total}
