# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    qr_a = cirq.LineQubit.range(0, 3)
    qr_b = cirq.LineQubit.range(3, 6)
    ancillary = cirq.LineQubit.range(6, 9)
    
    circuit = cirq.Circuit()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2-i] == '1':
            circuit.append(cirq.X(qr_b[i]))
            
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
        
    circuit.append(cirq.measure(ancillary[2], ancillary[1], ancillary[0], key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    
    counts = {}
    total = 0
    for bits in result.measurements['m']:
        bitstring = ''.join(str(b) for b in bits)
        counts[bitstring] = counts.get(bitstring, 0) + 1
        total += 1
        
    return {k: v / total for k, v in counts.items()}
