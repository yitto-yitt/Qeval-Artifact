# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    
    # Apply X gates to qubits corresponding to 1-bits in a
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
            
    # Apply X gates to qubits corresponding to 1-bits in b
    for i in range(8):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
            
    # Measure qubits in reverse order to match Qiskit's MSB-first string representation
    circuit.append(cirq.measure(*qubits[::-1], key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    
    measurements = result.measurements['m']
    counts = {}
    for row in measurements:
        bitstring = "".join(str(bit) for bit in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
