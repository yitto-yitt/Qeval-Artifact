# EVAL_META: task_id=14, framework=cirq, class=1
import cirq

def bell_each_shot():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    ])
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    histogram = result.histogram(key='result')
    counts = {
        format(outcome, '02b'): count
        for outcome, count in histogram.items()
    }
    total = 10
    return {bitstring: count / total for bitstring, count in counts.items()}
