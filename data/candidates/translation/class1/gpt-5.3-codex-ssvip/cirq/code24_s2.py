# EVAL_META: task_id=24, framework=cirq, class=1
import cirq


def dj_algorithm(oracle):
    qubits = sorted(oracle.all_qubits())
    n = len(qubits)

    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[n - 1]))
    circuit.append(cirq.H.on_each(*qubits))
    circuit += oracle
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(cirq.measure(*qubits[: n - 1], key="c"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=4096)
    histogram = result.multi_measurement_histogram(keys=["c"])

    total = sum(histogram.values())
    probs = {}
    for key_tuple, count in histogram.items():
        bits = "".join(str(b) for b in key_tuple)
        probs[bits] = count / total
    return probs
