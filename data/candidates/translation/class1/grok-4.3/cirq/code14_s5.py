# EVAL_META: task_id=14, framework=cirq, class=1
import cirq

def bell_each_shot():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    meas = result.measurements['meas']
    counts = {}
    for row in meas:
        key = ''.join(str(bit) for bit in row)
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
