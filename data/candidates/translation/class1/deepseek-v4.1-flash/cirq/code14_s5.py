# EVAL_META: task_id=14, framework=cirq, class=1
import cirq

def bell_each_shot():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)

    counts = {}
    for bits in result.measurements['m']:
        key = ''.join(str(int(b)) for b in bits)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
