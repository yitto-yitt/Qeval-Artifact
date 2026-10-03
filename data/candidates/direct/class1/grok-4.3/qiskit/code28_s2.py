# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def visualize_bell_states():
    sim = AerSimulator()
    qc_plus = QuantumCircuit(2, 2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure(0, 0)
    qc_plus.measure(1, 1)
    qc_minus = QuantumCircuit(2, 2)
    qc_minus.h(0)
    qc_minus.cx(0, 1)
    qc_minus.z(0)
    qc_minus.measure(0, 0)
    qc_minus.measure(1, 1)
    res_plus = sim.run(transpile(qc_plus, sim), shots=4096, seed_simulator=42).result()
    res_minus = sim.run(transpile(qc_minus, sim), shots=4096, seed_simulator=42).result()
    counts_plus = res_plus.get_counts()
    counts_minus = res_minus.get_counts()
    def to_probs(counts):
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}
    return {'phi_plus': to_probs(counts_plus), 'phi_minus': to_probs(counts_minus)}
