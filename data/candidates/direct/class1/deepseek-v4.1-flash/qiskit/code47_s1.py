# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def random_coin_flip(samples):
    if samples <= 0:
        return {"Heads": 0.5, "Tails": 0.5}

    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    backend = AerSimulator()
    result = backend.run(qc, shots=samples).result()
    counts = result.get_counts()

    heads = counts.get("0", 0) / samples
    tails = 1.0 - heads

    return {"Heads": heads, "Tails": tails}
