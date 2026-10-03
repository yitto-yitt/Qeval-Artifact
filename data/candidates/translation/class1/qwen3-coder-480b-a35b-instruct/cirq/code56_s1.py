# EVAL_META: task_id=56, framework=cirq, class=1
import cirq
import collections

def not_gate(a):
    # Create a quantum circuit with 8 qubits
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    
    # Convert input to 8-bit binary string
    a_binary = format(a, "08b")
    
    # Apply X gates for bits that are '0' in the input
    for i in range(8):
        if a_binary[7-i] == "0":
            circuit.append(cirq.X(qubits[i]))
    
    # Add measurements to all qubits
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    
    # Get measurement results
    measurements = result.data['result'].map(lambda x: format(x, '08b')).value_counts()
    
    # Convert to probability distribution
    total = sum(measurements.values)
    return {key: value / total for key, value in measurements.items()}
