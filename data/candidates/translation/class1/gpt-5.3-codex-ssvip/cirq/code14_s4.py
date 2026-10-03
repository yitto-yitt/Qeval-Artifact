# EVAL_META: task_id=14, framework=cirq, class=1
import cirq


def bell_each_shot():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="meas"),
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    counts = result.multi_measurement_histogram(keys=["meas"])
    total = sum(counts.values())
    return {"".join(str(bit) for bit in bits): count / total for bits, count in counts.items()}
