# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
from collections import Counter

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    
    # Phi plus circuit
    phi_plus = cirq.Circuit()
    phi_plus.append(cirq.H(q0))
    phi_plus.append(cirq.CNOT(q0, q1))
    phi_plus.append(cirq.measure(q1, q0, key='meas'))
    
    # Phi minus circuit
    phi_minus = cirq.Circuit()
    phi_minus.append(cirq.X(q0))
    phi_minus.append(cirq.H(q0))
    phi_minus.append(cirq.CNOT(q0, q1))
    phi_minus.append(cirq.measure(q1, q0, key='meas'))
    
    simulator = cirq.Simulator()
    
    # Run phi_plus
    result_plus = simulator.run(phi_plus, repetitions=1000)
    measurements_plus = result_plus.measurements['meas']
    counts_plus = Counter("".join(map(str, row)) for row in measurements_plus)
    
    # Run phi_minus
    result_minus = simulator.run(phi_minus, repetitions=1000)
    measurements_minus = result_minus.measurements['meas']
    counts_minus = Counter("".join(map(str, row)) for row in measurements_minus)
    
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    return {
        "phi_plus": {key: val / total_plus for key, val in counts_plus.items()},
        "phi_minus": {key: val / total_minus for key, val in counts_minus.items()}
    }
