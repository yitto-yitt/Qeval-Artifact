# EVAL_META: task_id=14, framework=cirq, class=1
import cirq

def bell_each_shot():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(*qubits, key='meas')
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    counts = {}
    for bits in result.measurements['meas']:
        bitstring = ''.join(str(bit) for bit in reversed(bits))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
