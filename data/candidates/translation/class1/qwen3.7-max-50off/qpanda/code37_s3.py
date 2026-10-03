# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QuantumCircuit, X, H, CNOT, Measure

def bv_algorithm(s):
    n = len(s)
    qm = QMachine()
    q = qm.qAlloc_many(n + 1)
    c = qm.cAlloc_many(n)
    
    qc = QuantumCircuit()
    qc << X(q[n])
    for i in range(n + 1):
        qc << H(q[i])
        
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CNOT(q[index], q[n])
            
    for i in range(n):
        qc << H(q[i])
        
    for i in range(n):
        qc << Measure(q[i], c[i])
        
    result = qm.run_with_configuration(qc, c, 1)
    bitstrings = list(result.keys())
    return [bitstrings, result]
