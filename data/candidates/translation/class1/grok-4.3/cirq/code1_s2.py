# EVAL_META: task_id=1, framework=cirq, class=1
import cirq

def run_bell_state_simulator():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(qubits[0], qubits[1], key='result')
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    samples = result.measurements['result']
    counts = {}
    for sample in samples:
        bitstring = ''.join(str(int(bit)) for bit in sample)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
