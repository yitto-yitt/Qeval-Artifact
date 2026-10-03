# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def random_coin_flip(samples):
    """Simulate a quantum coin flip and return the probability distribution."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    simulator = AerSimulator()
    job = simulator.run(qc, shots=samples)
    counts = job.result().get_counts(qc)

    total = sum(counts.values())
    heads = counts.get("0", 0) / total
    tails = counts.get("1", 0) / total

    return {"Heads": heads, "Tails": tails}
