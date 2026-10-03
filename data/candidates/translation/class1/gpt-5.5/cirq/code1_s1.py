# EVAL_META: task_id=1, framework=cirq, class=1
import cirq


def run_bell_state_simulator():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="meas"),
    )

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)

    counts = {}
    measurements = result.measurements["meas"]
    for row in measurements:
        bitstring = "".join(str(int(bit)) for bit in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
