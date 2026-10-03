# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    
    # phi_plus
    circuit_plus = cirq.Circuit()
    circuit_plus.append(cirq.H(q0))
    circuit_plus.append(cirq.CNOT(q0, q1))
    circuit_plus.append(cirq.measure(q1, q0, key='m'))
    
    # phi_minus
    circuit_minus = cirq.Circuit()
    circuit_minus.append(cirq.X(q0))
    circuit_minus.append(cirq.H(q0))
    circuit_minus.append(cirq.CNOT(q0, q1))
    circuit_minus.append(cirq.measure(q1, q0, key='m'))
    
    simulator = cirq.Simulator()
    
    result_plus = simulator.run(circuit_plus, repetitions=1000)
    result_minus = simulator.run(circuit_minus, repetitions=1000)
    
    counts_plus = result_plus.histogram(key='m')
    counts_minus = result_minus.histogram(key='m')
    
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    phi_plus_dist = {f"{k:02b}": v / total_plus for k, v in counts_plus.items()}
    phi_minus_dist = {f"{k:02b}": v / total_minus for k, v in counts_minus.items()}
    
    return {
        "phi_plus": phi_plus_dist,
        "phi_minus": phi_minus_dist
    }
