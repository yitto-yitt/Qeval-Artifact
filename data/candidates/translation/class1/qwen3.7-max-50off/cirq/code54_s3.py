# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i + 3) for i in range(3)]
    anc = [cirq.LineQubit(i + 6) for i in range(3)]
    
    circuit = cirq.Circuit()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2 - i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_str[2 - i] == '1':
            circuit.append(cirq.X(qr_b[i]))
            
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], anc[i]))
        
    circuit.append(cirq.measure(anc[2], anc[1], anc[0], key='measure'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    
    measurements = result.measurements['measure']
    total = len(measurements)
    counts = {}
    for m in measurements:
        key = ''.join(str(int(x)) for x in m)
        counts[key] = counts.get(key, 0) + 1
        
    return {k: v / total for k, v in counts.items()}
