# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    
    phi_plus_circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    ])
    
    phi_minus_circuit = cirq.Circuit([
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    ])
    
    sim = cirq.Simulator()
    
    res_plus = sim.run(phi_plus_circuit, repetitions=1000)
    res_minus = sim.run(phi_minus_circuit, repetitions=1000)
    
    def get_probs(measurements):
        counts = {}
        for row in measurements:
            s = f"{row[1]}{row[0]}"
            counts[s] = counts.get(s, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    return {
        "phi_plus": get_probs(res_plus.measurements['m']),
        "phi_minus": get_probs(res_minus.measurements['m'])
    }
