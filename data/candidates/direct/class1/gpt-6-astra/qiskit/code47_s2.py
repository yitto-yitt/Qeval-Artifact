# EVAL_META: task_id=47, framework=qiskit, class=1
from operator import index

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def random_coin_flip(samples):
    samples = index(samples)
    if samples <= 0:
        raise ValueError("samples must be a positive integer.")

    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)

    counts = AerSimulator().run(circuit, shots=samples).result().get_counts()
    heads = counts.get("0", 0) / sum(counts.values())
    return {"Heads": heads, "Tails": 1.0 - heads}
