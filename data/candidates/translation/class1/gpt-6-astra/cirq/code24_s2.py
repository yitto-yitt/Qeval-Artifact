# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
from collections import Counter

def dj_algorithm(oracle):
    oracle_circuit = cirq.Circuit(oracle)
    qubits = list(cirq.QubitOrder.DEFAULT.order_for(oracle_circuit.all_qubits()))
    n = len(qubits)
    if n == 0:
        raise ValueError("The oracle must contain an output qubit.")

    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[-1]))
    circuit.append(cirq.H.on_each(*qubits))
    circuit += oracle_circuit
    circuit.append(cirq.H.on_each(*qubits))

    key = "_dj_inputs"
    existing_keys = cirq.measurement_key_names(oracle_circuit)
    while key in existing_keys:
        key += "_"

    circuit.append(cirq.measure(*(qubits[:-1] or qubits), key=key))
    result = cirq.Simulator().run(circuit, repetitions=1024)
    counts = Counter(
        "".join(str(int(bit)) for bit in row[:n - 1][::-1])
        for row in result.measurements[key]
    )
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
