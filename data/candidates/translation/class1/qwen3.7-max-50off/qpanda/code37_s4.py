# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    
    qc.x(n)
    for i in range(n + 1):
        qc.h(i)
        
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, n)
            
    for i in range(n):
        qc.h(i)
        
    for i in range(n):
        qc.measure(i, i)
        
    machine = QMachine()
    result = machine.execute(qc, shots=1)
    
    if isinstance(result, dict):
        bitstrings = list(result.keys())
    elif hasattr(result, 'get_counts'):
        bitstrings = list(result.get_counts().keys())
    else:
        bitstrings = [str(result)]
        
    return [bitstrings, result]
