# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(*qubits, key='meas')
    )
    noise = cirq.depolarize(p=0.01)
    noisy_circuit = circuit.with_noise(noise)
    simulator = cirq.Simulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    return {format(k, '02b'): v / total for k, v in counts.items()}
