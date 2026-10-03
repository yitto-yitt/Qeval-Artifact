# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def random_coin_flip(samples):
    shots = int(samples)
    if shots <= 0:
        return {"Heads": 0.5, "Tails": 0.5}

    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)

    simulator = AerSimulator()
    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts(circuit)

    heads = counts.get("0", 0)
    heads_probability = heads / shots

    return {"Heads": heads_probability, "Tails": 1.0 - heads_probability}
