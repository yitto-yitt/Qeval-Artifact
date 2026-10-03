# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
from collections import Counter

def bell_each_shot():
    # Define qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Create circuit
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    
    # Simulate the circuit for 10 shots
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    measurements = result.measurements['m']
    
    # Convert to bitstrings matching Qiskit's endianness (qubit 0 is LSB / rightmost)
    bitstrings = [f"{shot[1]}{shot[0]}" for shot in measurements]
    counts = Counter(bitstrings)
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
