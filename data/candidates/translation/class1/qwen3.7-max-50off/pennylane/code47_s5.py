# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device("default.qubit", shots=samples)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(wires=0)
        
    results = circuit()
    total = len(results)
    heads = sum(1 for x in results if x == 0)
    tails = total - heads
    
    return {'Heads': heads / total, 'Tails': tails / total}
