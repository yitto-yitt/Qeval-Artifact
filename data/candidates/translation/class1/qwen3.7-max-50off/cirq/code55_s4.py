# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    qubits = cirq.LineQubit.range(9)
    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    circuit = cirq.Circuit()
    
    for i in range(3):
        if a_bin[2-i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2-i] == '0':
            circuit.append(cirq.X(qr_b[i]))
            
    for i in range(3):
        circuit.append(cirq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
        
    for i in range(3):
        circuit.append(cirq.X(ancillary[i]))
        
    circuit.append(cirq.measure(*ancillary, key='measure'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    
    counts = {}
    for row in result.measurements['measure']:
        s = f"{row[2]}{row[1]}{row[0]}"
        counts[s] = counts.get(s, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
