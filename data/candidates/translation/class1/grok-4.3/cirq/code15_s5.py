# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    noise = cirq.depolarize(p=0.01)
    simulator = cirq.DensityMatrixSimulator(noise=noise)
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    return {format(state, '02b'): count / total for state, count in counts.items()}
