# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    qubits = cirq.LineQubit.range(2)
    phi_plus = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(*qubits, key='meas')
    )
    phi_minus = cirq.Circuit(
        cirq.X(qubits[0]),
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(*qubits, key='meas')
    )
    simulator = cirq.Simulator()
    result_plus = simulator.run(phi_plus, repetitions=1000)
    result_minus = simulator.run(phi_minus, repetitions=1000)
    def get_prob_dict(result):
        measurements = result.measurements['meas']
        counts = {}
        for meas in measurements:
            bitstring = ''.join(map(str, meas))
            counts[bitstring] = counts.get(bitstring, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}
    return {
        "phi_plus": get_prob_dict(result_plus),
        "phi_minus": get_prob_dict(result_minus)
    }
