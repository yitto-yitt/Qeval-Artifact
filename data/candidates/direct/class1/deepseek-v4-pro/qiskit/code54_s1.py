# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def and_gate(a, b):
    qc = QuantumCircuit(9, 3)
    # encode a (qubits 0-2)
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
    # encode b (qubits 3-5)
    for i in range(3):
        if (b >> i) & 1:
            qc.x(3 + i)
    # bitwise AND using Toffoli gates (output qubits 6-8)
    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)
    # measure output qubits
    qc.measure([6, 7, 8], [0, 1, 2])
    # simulate
    sim = AerSimulator()
    job = sim.run(qc, shots=1024)
    counts = job.result().get_counts()
    # build probability distribution with all 8 keys
    prob_dist = {f'{i:03b}': 0.0 for i in range(8)}
    total = sum(counts.values())
    for k, v in counts.items():
        prob_dist[k] = v / total
    return prob_dist
