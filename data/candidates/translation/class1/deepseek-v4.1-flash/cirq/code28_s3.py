# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
from collections import Counter

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    
    phi_plus = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    
    phi_minus = cirq.Circuit(
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    
    simulator = cirq.Simulator()
    shots = 1000
    
    res_plus = simulator.run(phi_plus, repetitions=shots)
    res_minus = simulator.run(phi_minus, repetitions=shots)
    
    def to_probs(result):
        counts = Counter()
        for shot in result.measurements['m']:
            # Qiskit-like bitstring order: qubit 1 then qubit 0
            bitstring = f"{int(shot[1])}{int(shot[0])}"
            counts[bitstring] += 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}
    
    return {
        "phi_plus": to_probs(res_plus),
        "phi_minus": to_probs(res_minus),
    }
