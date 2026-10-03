# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit
try:
    from pyqpanda3.core import QMachine
except ImportError:
    from pyqpanda3.core import OriginQMachine as QMachine

def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    ancilla = n

    qc.x(ancilla)
    for i in range(n + 1):
        qc.h(i)
        
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, ancilla)
            
    for i in range(n):
        qc.h(i)
        
    for i in range(n):
        qc.measure(i, i)

    machine = QMachine()
    result = machine.run(qc, 1)
    
    if isinstance(result, dict):
        bitstrings = list(result.keys())
    else:
        bitstrings = list(result.keys()) if hasattr(result, 'keys') else [str(result)]
        
    return [bitstrings, result]
