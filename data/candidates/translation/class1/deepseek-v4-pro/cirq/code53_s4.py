# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
import numpy as np

def xor_gate(a, b):
    # 8 qubits
    qubits = cirq.LineQubit.range(8)
    
    # Build the circuit
    circuit = cirq.Circuit()
    
    # Apply XOR with a: flip qubits where a has 1s
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    
    # Apply XOR with b: flip qubits where b has 1s
    for i in range(8):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    
    # Measure all qubits
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='result')
    
    # Convert to bitstrings and normalize
    total = sum(counts.values())
    prob_dist = {}
    for outcome, count in counts.items():
        bitstring = format(outcome, '08b')
        prob_dist[bitstring] = count / total
    
    return prob_dist
