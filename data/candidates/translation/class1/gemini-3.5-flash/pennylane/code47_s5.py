# EVAL_META: task_id=47, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def random_coin_flip(samples):
    dev = qml.device('default.qubit', wires=1, shots=samples)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(wires=0)
        
    res = np.atleast_1d(circuit())
    num_zeros = np.count_nonzero(res == 0)
    num_ones = np.count_nonzero(res == 1)
    total = len(res)
    return {'Heads': float(num_zeros) / total, 'Tails': float(num_ones) / total}
