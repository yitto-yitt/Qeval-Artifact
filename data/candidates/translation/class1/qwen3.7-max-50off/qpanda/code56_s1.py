# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, Sampler

def not_gate(a):
    qc = QuantumCircuit(8)
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            qc.x(i)
    qc.measure_all()
    
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
