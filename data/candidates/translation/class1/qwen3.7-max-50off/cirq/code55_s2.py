# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    qr_a = cirq.LineQubit.range(0, 3)
    qr_b = cirq.LineQubit.range(3, 6)
    ancillary = cirq.LineQubit.range(6, 9)
    
    circuit = cirq.Circuit()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_bin[2-i] == '0':
            circuit.append(cirq.X(qr_b[i]))
            
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
        
    for i in range(3):
        circuit.append(cirq.X(ancillary[i]))
        
    circuit.append(cirq.measure(*ancillary, key='m'))
    
    simulator = cirq.Simulator()
    repetitions = 1024
    result = simulator.run(circuit, repetitions=repetitions)
    
    counts = {}
    for meas in result.measurements['m']:
        bitstring = "".join(str(int(bit)) for bit in reversed(meas))
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
