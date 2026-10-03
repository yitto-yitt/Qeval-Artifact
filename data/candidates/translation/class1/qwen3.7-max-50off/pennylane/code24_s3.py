# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def dj_algorithm(oracle):
    if hasattr(oracle, 'shape'):
        n = int(np.round(np.log2(oracle.shape[0])))
    elif hasattr(oracle, 'num_wires'):
        n = oracle.num_wires
    elif hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
    else:
        n = int(np.round(np.log2(len(oracle))))
        
    dev = qml.device("default.qubit", wires=n)
    
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for i in range(n):
            qml.Hadamard(wires=i)
            
        if callable(oracle) and not hasattr(oracle, 'shape'):
            try:
                oracle(wires=list(range(n)))
            except TypeError:
                oracle()
        else:
            if hasattr(oracle, 'matrix'):
                mat = oracle.matrix()
            else:
                mat = np.array(oracle)
            qml.QubitUnitary(mat, wires=list(range(n)))
            
        for i in range(n):
            qml.Hadamard(wires=i)
            
        return qml.probs(wires=list(range(n-1)))
        
    probs = circuit()
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-12:
            pl_bs = format(i, f'0{n-1}b')
            qk_bs = pl_bs[::-1]
            result[qk_bs] = float(p)
            
    return result
