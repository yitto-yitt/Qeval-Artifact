# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
def dj_algorithm(oracle):
    n = cirq.num_qubits(oracle)
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit(
        cirq.X(qubits[-1]),
        cirq.H.on_each(qubits),
        oracle.on(*qubits),
        cirq.H.on_each(qubits)
    )
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    probs = cirq.state_vector_to_probabilities(result.final_state_vector)
    m = n - 1
    dist = {}
    for i in range(1 << m):
        p = probs[(i << 1)] + probs[(i << 1) | 1]
        if p > 0:
            dist[format(i, f'0{m}b')] = float(p)
    return dist
