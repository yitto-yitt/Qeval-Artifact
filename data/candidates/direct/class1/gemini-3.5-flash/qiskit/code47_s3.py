# EVAL_META: task_id=47, framework=qiskit, class=1
import qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def random_coin_flip(samples: int) -> dict:
    if samples <= 0:
        return {'Heads': 0.5, 'Tails': 0.5}
        
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    
    backend = AerSimulator()
    job = backend.run(qc, shots=samples)
    result = job.result()
    counts = result.get_counts()
    
    heads_count = counts.get('0', 0)
    tails_count = counts.get('1', 0)
    total = heads_count + tails_count
    
    if total == 0:
        return {'Heads': 0.5, 'Tails': 0.5}
        
    return {
        'Heads': heads_count / total,
        'Tails': tails_count / total
    }
