# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, Simulator

def not_gate(a):
    qc = QuantumCircuit(8, 8)
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            qc.x(i)
            
    for i in range(8):
        qc.measure(i, i)
        
    sim = Simulator()
    counts = sim.run(qc, 1024)
    
    total = sum(counts.values())
    return {str(k): v / total for k, v in counts.items()}
