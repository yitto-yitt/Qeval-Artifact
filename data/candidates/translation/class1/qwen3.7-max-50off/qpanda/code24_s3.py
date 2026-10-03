# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QCircuit, QPU, X, H, Measure

def dj_algorithm(oracle):
    if hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
    elif hasattr(oracle, 'qubit_num'):
        n = oracle.qubit_num
    elif hasattr(oracle, 'qubits'):
        n = len(oracle.qubits)
    else:
        n = 4
        
    qm = QMachine()
    qubits = qm.qubits(n)
    cbits = qm.cbits(n - 1)
    
    qc = QCircuit()
    qc << X(qubits[n-1])
    for i in range(n):
        qc << H(qubits[i])
        
    qc << oracle
    
    for i in range(n):
        qc << H(qubits[i])
        
    for i in range(n - 1):
        qc << Measure(qubits[i], cbits[i])
        
    qpu = QPU()
    try:
        result = qpu.run(qc, qm, 100000)
    except TypeError:
        result = qpu.run(qc, qm, shots=100000)
        
    counts = result.get_counts()
    total = sum(counts.values())
    
    probs = {}
    for k, v in counts.items():
        if isinstance(k, int):
            k = format(k, f'0{n-1}b')
        probs[k] = v / total
        
    return probs
