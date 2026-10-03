# EVAL_META: task_id=56, framework=cirq, class=1
import cirq


def not_gate(a):
    qubits = [cirq.LineQubit(i) for i in range(8)]
    circuit = cirq.Circuit()
    bits = format(a, "08b")
    for i in range(8):
        if bits[7 - i] == "0":
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key="meas"))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    histogram = result.multi_measurement_histogram(keys=["meas"])
    total = sum(histogram.values())
    probs = {}
    for (meas_bits,), count in histogram.items():
        key = "".join(str(b) for b in reversed(meas_bits))
        probs[key] = count / total
    return probs
