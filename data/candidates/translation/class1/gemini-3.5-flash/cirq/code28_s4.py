# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q = cirq.LineQubit.range(2)
    
    # phi_plus
    phi_plus_circuit = cirq.Circuit()
    phi_plus_circuit.append(cirq.H(q[0]))
    phi_plus_circuit.append(cirq.CNOT(q[0], q[1]))
    phi_plus_circuit.append(cirq.measure(q[1], q[0], key='m'))
    
    # phi_minus
    phi_minus_circuit = cirq.Circuit()
    phi_minus_circuit.append(cirq.X(q[0]))
    phi_minus_circuit.append(cirq.H(q[0]))
    phi_minus_circuit.append(cirq.CNOT(q[0], q[1]))
    phi_minus_circuit.append(cirq.measure(q[1], q[0], key='m'))
    
    simulator = cirq.Simulator()
    
    # run phi_plus
    result_plus = simulator.run(phi_plus_circuit, repetitions=1000)
    hist_plus = result_plus.histogram(key='m')
    total_plus = sum(hist_plus.values())
    phi_plus_dist = {f"{val:02b}": count / total_plus for val, count in hist_plus.items()}
    
    # run phi_minus
    result_minus = simulator.run(phi_minus_circuit, repetitions=1000)
    hist_minus = result_minus.histogram(key='m')
    total_minus = sum(hist_minus.values())
    phi_minus_dist = {f"{val:02b}": count / total_minus for val, count in hist_minus.items()}
    
    return {
        "phi_plus": phi_plus_dist,
        "phi_minus": phi_minus_dist
    }
