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
    hist = result.multi_measurement_histogram(keys=["c"])

    total = sum(hist.values())
    probs = {}
    for key_tuple, count in hist.items():
        bits = key_tuple[0]
        bitstring = format(bits, f"0{n-1}b")[::-1]
        probs[bitstring] = count / total
    return probs
