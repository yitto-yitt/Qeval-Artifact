# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def random_coin_flip(samples):
    shots = int(samples)
    if shots <= 0:
        return {"Heads": 0.0, "Tails": 0.0}

    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)

    backend = AerSimulator()
    compiled = transpile(circuit, backend)
    result = backend.run(compiled, shots=shots).result()
    counts = result.get_counts(compiled)

    heads = counts.get("0", 0) / shots
    tails = counts.get("1", 0) / shots

    total = heads + tails
    if total != 1.0 and total > 0:
        tails = 1.0 - heads

    return {"Heads": heads, "Tails": tails}
