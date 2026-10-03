# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    noisy_circuit = circuit.with_noise(cirq.depolarize(p=0.02))
    simulator = cirq.Simulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    return {f"{val:02b}": count / total for val, count in counts.items()}
