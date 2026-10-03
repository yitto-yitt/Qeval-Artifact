# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    
    # Phi plus
    circuit_plus = cirq.Circuit()
    circuit_plus.append(cirq.H(q0))
    circuit_plus.append(cirq.CNOT(q0, q1))
    circuit_plus.append(cirq.measure(q0, q1, key='m'))
    
    # Phi minus
    circuit_minus = cirq.Circuit()
    circuit_minus.append(cirq.X(q0))
    circuit_minus.append(cirq.H(q0))
    circuit_minus.append(cirq.CNOT(q0, q1))
    circuit_minus.append(cirq.measure(q0, q1, key='m'))
    
    simulator = cirq.Simulator()
    
    result_plus = simulator.run(circuit_plus, shots=1000)
    counts_plus = result_plus.histogram(key='m')
    total_plus = sum(counts_plus.values())
    dist_plus = {f"{val:02b}": count / total_plus for val, count in counts_plus.items()}
    
    result_minus = simulator.run(circuit_minus, shots=1000)
    counts_minus = result_minus.histogram(key='m')
    total_minus = sum(counts_minus.values())
    dist_minus = {f"{val:02b}": count / total_minus for val, count in counts_minus.items()}
    
    return {
        "phi_plus": dist_plus,
        "phi_minus": dist_minus
    }
