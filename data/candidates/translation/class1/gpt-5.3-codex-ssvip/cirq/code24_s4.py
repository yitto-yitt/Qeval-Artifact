# EVAL_META: task_id=24, framework=cirq, class=1
import cirq


def dj_algorithm(oracle):
    qubits = sorted(oracle.all_qubits())
    n = len(qubits)
    input_qubits = qubits[: n - 1]
    output_qubit = qubits[n - 1]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append(cirq.H.on_each(*qubits))
    circuit += oracle
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(cirq.measure(*input_qubits, key="c"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=4096)
    histogram = result.multi_measurement_histogram(keys=["c"])

    total = sum(histogram.values())
    probs = {}
    for key, count in histogram.items():
        bits = key[0]
        bitstring = "".join(str(b) for b in bits[::-1])
        probs[bitstring] = count / total
    return probs
