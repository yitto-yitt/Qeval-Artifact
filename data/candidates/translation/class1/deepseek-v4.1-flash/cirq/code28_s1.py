# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
import collections

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    
    phi_plus = cirq.Circuit()
    phi_plus.append(cirq.H(q0))
    phi_plus.append(cirq.CNOT(q0, q1))
    phi_plus.append(cirq.measure(q0, q1, key='m'))
    
    phi_minus = cirq.Circuit()
    phi_minus.append(cirq.X(q0))
    phi_minus.append(cirq.H(q0))
    phi_minus.append(cirq.CNOT(q0, q1))
    phi_minus.append(cirq.measure(q0, q1, key='m'))
    
    simulator = cirq.Simulator()
    result_phi_plus = simulator.run(phi_plus, repetitions=1000)
    result_phi_minus = simulator.run(phi_minus, repetitions=1000)
    
    counts_phi_plus = collections.Counter(
        ''.join(str(int(b)) for b in row)
        for row in result_phi_plus.measurements['m']
    )
    counts_phi_minus = collections.Counter(
        ''.join(str(int(b)) for b in row)
        for row in result_phi_minus.measurements['m']
    )
    
    total_phi_plus = sum(counts_phi_plus.values())
    total_phi_minus = sum(counts_phi_minus.values())
    
    return {
        "phi_plus": {key: value / total_phi_plus for key, value in counts_phi_plus.items()},
        "phi_minus": {key: value / total_phi_minus for key, value in counts_phi_minus.items()},
    }
