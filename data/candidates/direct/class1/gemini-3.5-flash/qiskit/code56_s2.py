# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def not_gate(a: int) -> dict:
    qc = QuantumCircuit(8)
    for i in range(8):
        bit = (a >> i) & 1
        if bit == 0:
            qc.x(i)
    qc.measure_all()
    
    backend = AerSimulator()
    job = backend.run(transpile(qc, backend), shots=1024)
    counts = job.result().get_counts()
    
    total_shots = sum(counts.values())
    prob_dist = {k: v / total_shots for k, v in counts.items()}
    return prob_dist
