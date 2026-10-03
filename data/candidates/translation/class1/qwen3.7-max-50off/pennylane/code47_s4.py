# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1, shots=samples)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(wires=0)
    
    results = circuit()
    heads = sum(1 for x in results if x == 0)
    tails = sum(1 for x in results if x == 1)
    total = heads + tails
    
    return {'Heads': heads / total, 'Tails': tails / total}
