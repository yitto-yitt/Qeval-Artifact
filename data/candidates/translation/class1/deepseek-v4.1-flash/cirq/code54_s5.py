# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    a_qubits = [cirq.NamedQubit(f'a{i}') for i in range(3)]
    b_qubits = [cirq.NamedQubit(f'b{i}') for i in range(3)]
    ancilla = [cirq.NamedQubit(f'anc{i}') for i in range(3)]
    
    circuit = cirq.Circuit()
    
    for i in range(3):
        if (a >> i) & 1:
            circuit.append(cirq.X(a_qubits[i]))
        if (b >> i) & 1:
            circuit.append(cirq.X(b_qubits[i]))
    
    for i in range(3):
        circuit.append(cirq.TOFFOLI(a_qubits[i], b_qubits[i], ancilla[i]))
    
    # Measure ancilla in MSB-to-LSB order to match Qiskit's bitstring ordering
    circuit.append(cirq.measure(ancilla[2], ancilla[1], ancilla[0], key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    
    measurements = result.measurements['m']
    counts = {}
    for row in measurements:
        bitstring = ''.join(str(int(bit)) for bit in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
