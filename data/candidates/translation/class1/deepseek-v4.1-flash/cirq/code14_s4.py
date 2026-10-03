# EVAL_META: task_id=14, framework=cirq, class=1
import cirq

def bell_each_shot():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas'),
    )

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    counts = result.histogram(key='meas')

    total = sum(counts.values())
    return {format(bits, '02b'): value / total for bits, value in counts.items()}
