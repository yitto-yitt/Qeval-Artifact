# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml

def random_coin_flip(samples):
    dev = qml.device("default.qubit", wires=1, shots=samples)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(wires=0)
    
    samples = circuit()
    heads_count = sum(samples == 0)
    tails_count = sum(samples == 1)
    total = len(samples)
    
    return {'Heads': heads_count / total, 'Tails': tails_count / total}
