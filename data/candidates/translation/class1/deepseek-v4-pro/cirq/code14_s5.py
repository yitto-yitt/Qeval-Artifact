# EVAL_META: task_id=14, framework=cirq, class=1
import cirq

def bell_each_shot():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result'),
    ])
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    counts = result.histogram(key='result')
    total = sum(counts.values())
    return {format(k, 'b').zfill(2): v / total for k, v in counts.items()}
