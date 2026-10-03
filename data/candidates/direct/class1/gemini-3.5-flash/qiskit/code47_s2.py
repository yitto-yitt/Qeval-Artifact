# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def random_coin_flip(samples: int) -> dict:
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    
    simulator = AerSimulator()
    t_qc = transpile(qc, simulator)
    result = simulator.run(t_qc, shots=samples).result()
    counts = result.get_counts(t_qc)
    
    c0 = counts.get('0', 0)
    c1 = counts.get('1', 0)
    total = c0 + c1
    
    if total == 0:
        return {'Heads': 0.5, 'Tails': 0.5}
    
    return {
        'Heads': float(c0) / total,
        'Tails': float(c1) / total
    }
