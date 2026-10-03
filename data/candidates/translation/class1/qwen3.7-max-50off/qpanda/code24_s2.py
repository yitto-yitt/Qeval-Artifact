# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, QCircuit, H, X, Measure

def dj_algorithm(oracle):
    n = None
    qubits = None
    
    if hasattr(oracle, 'qubits') and oracle.qubits:
        qubits = list(oracle.qubits)
        n = len(qubits)
    elif hasattr(oracle, 'get_qubits'):
        qubits = list(oracle.get_qubits())
        n = len(qubits)
    elif hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
    elif hasattr(oracle, 'qubit_num'):
        n = oracle.qubit_num
        
    qm = QuantumMachine()
    if qubits is None:
        if n is None:
            n = 4
        qubits = qm.qAlloc_many(n)
        
    prog = QProg()
    prog << X(qubits[n - 1])
    for i in range(n):
        prog << H(qubits[i])
        
    prog << oracle
    
    for i in range(n):
        prog << H(qubits[i])
        
    prob_dict = qm.prob_run_dict(prog, qubits[:n-1])
    
    return {k: v for k, v in prob_dict.items() if v > 1e-9}
