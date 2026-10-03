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
    hist = result.multi_measurement_histogram(keys=["meas"])
    total = sum(hist.values())
    return {"".join(str(bit) for bit in bits): count / total for bits, count in hist.items()}
