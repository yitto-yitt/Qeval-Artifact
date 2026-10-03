# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit, execute, Aer

def random_coin_flip(samples):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=samples).result()
    counts = result.get_counts(qc)
    
    heads_count = counts.get('0', 0)
    tails_count = counts.get('1', 0)
    
    total_shots = samples
    prob_heads = heads_count / total_shots
    prob_tails = tails_count / total_shots
    
    return {'Heads': prob_heads, 'Tails': prob_tails}
