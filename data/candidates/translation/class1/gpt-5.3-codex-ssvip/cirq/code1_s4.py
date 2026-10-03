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
    histogram = result.multi_measurement_histogram(keys=["meas"])
    total = sum(histogram.values())
    return {
        "".join(str(bit) for bit in bits): count / total
        for bits, count in histogram.items()
    }
