# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def random_coin_flip(samples: int) -> dict:
    if samples <= 0:
        return {'Heads': 0.5, 'Tails': 0.5}
    
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    
    backend = AerSimulator()
    t_qc = transpile(qc, backend)
    result = backend.run(t_qc, shots=samples).result()
    counts = result.get_counts()
    
    heads_count = counts.get('0', 0)
    heads_prob = heads_count / samples
    tails_prob = 1.0 - heads_prob
    
    return {'Heads': heads_prob, 'Tails': tails_prob}
