# EVAL_META: task_id=56, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def not_gate(a: int) -> dict:
    qc = QuantumCircuit(8, 8)
    for i in range(8):
        if not ((a >> i) & 1):
            qc.x(i)
    qc.measure(range(8), range(8))
    
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    return probabilities
