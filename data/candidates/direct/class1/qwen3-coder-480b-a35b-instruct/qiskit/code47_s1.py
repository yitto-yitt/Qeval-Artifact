# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def random_coin_flip(samples):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=samples).result()
    counts = result.get_counts(compiled_circuit)
    
    heads_count = counts.get('0', 0)
    tails_count = counts.get('1', 0)
    
    return {
        'Heads': heads_count / samples,
        'Tails': tails_count / samples
    }
