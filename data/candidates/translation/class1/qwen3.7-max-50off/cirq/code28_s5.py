# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    
    phi_plus_circuit = cirq.Circuit()
    phi_plus_circuit.append(cirq.H(q0))
    phi_plus_circuit.append(cirq.CNOT(q0, q1))
    phi_plus_circuit.append(cirq.measure(q0, q1, key='m_plus'))
    
    phi_minus_circuit = cirq.Circuit()
    phi_minus_circuit.append(cirq.X(q0))
    phi_minus_circuit.append(cirq.H(q0))
    phi_minus_circuit.append(cirq.CNOT(q0, q1))
    phi_minus_circuit.append(cirq.measure(q0, q1, key='m_minus'))
    
    sim = cirq.Simulator()
    
    res_plus = sim.run(phi_plus_circuit, repetitions=1000)
    res_minus = sim.run(phi_minus_circuit, repetitions=1000)
    
    counts_plus = res_plus.histogram(key='m_plus')
    counts_minus = res_minus.histogram(key='m_minus')
    
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    dist_plus = {f"{k:02b}"[::-1]: v / total_plus for k, v in counts_plus.items()}
    dist_minus = {f"{k:02b}"[::-1]: v / total_minus for k, v in counts_minus.items()}
    
    return {
        "phi_plus": dist_plus,
        "phi_minus": dist_minus
    }
