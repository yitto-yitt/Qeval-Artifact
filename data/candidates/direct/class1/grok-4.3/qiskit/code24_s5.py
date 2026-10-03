# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def dj_algorithm(oracle):
    n = oracle.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(n)
    for i in range(n):
        qc.h(i)
    qc.append(oracle, range(n + 1))
    for i in range(n):
        qc.h(i)
    qc.measure(range(n), range(n))
    sim = AerSimulator()
    transpiled = transpile(qc, sim)
    result = sim.run(transpiled, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}
    return probs
