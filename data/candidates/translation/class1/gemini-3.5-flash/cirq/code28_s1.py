# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
import collections

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    
    # phi_plus
    circuit_plus = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    
    # phi_minus
    circuit_minus = cirq.Circuit(
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    
    simulator = cirq.Simulator()
    
    def get_probabilities(circuit):
        result = simulator.run(circuit, repetitions=1000)
        measurements = result.measurements['m']
        counts = collections.Counter()
        for row in measurements:
            # row[0] is q0, row[1] is q1.
            # Qiskit's bitstring representation is MSB-to-LSB (q1 q0).
            bitstring = f"{row[1]}{row[0]}"
            counts[bitstring] += 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}
        
    return {
        "phi_plus": get_probabilities(circuit_plus),
        "phi_minus": get_probabilities(circuit_minus)
    }
