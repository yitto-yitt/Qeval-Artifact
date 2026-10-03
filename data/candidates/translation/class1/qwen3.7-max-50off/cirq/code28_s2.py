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
    
    counts_plus = {}
    for row in res_plus.measurements['m']:
        bs = f"{int(row[1])}{int(row[0])}"
        counts_plus[bs] = counts_plus.get(bs, 0) + 1
        
    counts_minus = {}
    for row in res_minus.measurements['m']:
        bs = f"{int(row[1])}{int(row[0])}"
        counts_minus[bs] = counts_minus.get(bs, 0) + 1
        
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    return {
        "phi_plus": {k: v / total_plus for k, v in counts_plus.items()},
        "phi_minus": {k: v / total_minus for k, v in counts_minus.items()}
    }
