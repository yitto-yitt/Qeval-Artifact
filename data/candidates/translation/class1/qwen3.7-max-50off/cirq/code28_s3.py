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
    shots = 1000
    
    res_plus = sim.run(phi_plus_circuit, repetitions=shots)
    res_minus = sim.run(phi_minus_circuit, repetitions=shots)
    
    def get_probs(result):
        counts = {}
        for bits in result.measurements['m']:
            bitstring = f"{int(bits[1])}{int(bits[0])}"
            counts[bitstring] = counts.get(bitstring, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    return {
        "phi_plus": get_probs(res_plus),
        "phi_minus": get_probs(res_minus)
    }
