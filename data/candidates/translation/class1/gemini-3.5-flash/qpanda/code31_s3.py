# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
import pyqpanda3.core as pq

def sampler_qiskit() -> Dict[str, float]:
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0]) \
         << pq.CNOT(qubits[0], qubits[1]) \
         << pq.Measure(qubits[0], cbits[0]) \
         << pq.Measure(qubits[1], cbits[1])
    
    try:
        pq.set_random_seed(42)
    except AttributeError:
        pass
        
    counts = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
