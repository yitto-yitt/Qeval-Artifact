# EVAL_META: task_id=54, framework=cirq, class=1
import cirq
import collections

def and_gate(a, b):
    qr_a = [cirq.LineQubit(i) for i in range(3)]
    qr_b = [cirq.LineQubit(i+3) for i in range(3)]
    ancillary = [cirq.LineQubit(i+6) for i in range(3)]
    
    circuit = cirq.Circuit()
    
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    
    for i in range(3):
        if a_bits[2-i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_bits[2-i] == '1':
            circuit.append(cirq.X(qr_b[i]))
    
    for i in range(3):
        circuit.append(cirq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
    
    circuit.append(cirq.measure(*ancillary, key='result'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    counts = result.histogram(key='result')
    
    total = sum(counts.values())
    prob_dist = {}
    for key, value in counts.items():
        bitstring = format(key, '03b')
        prob_dist[bitstring] = value / total
    
    return prob_dist
