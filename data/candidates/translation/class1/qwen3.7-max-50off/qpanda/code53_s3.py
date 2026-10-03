# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def xor_gate(a, b):
    xor_val = a ^ b
    qc = QuantumCircuit(8)
    for i in range(8):
        if (xor_val >> i) & 1:
            qc.x(i)
        qc.measure(i, i)
        
    machine = QMachine()
    result = machine.run(qc, 1000)
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
