# EVAL_META: task_id=1, framework=cirq, class=1
import cirq
import numpy as np

def run_bell_state_simulator():
    # Create two qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Build the Bell state circuit: |Φ+⟩ = (|00⟩ + |11⟩)/√2
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    ])
    
    # Simulate with 1000 shots
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    
    # Extract measurement outcomes
    counts = result.histogram(key='result')
    
    # Convert to probability distribution
    total = sum(counts.values())
    # Format keys as bitstrings (e.g., 0 -> '00', 3 -> '11')
    return {format(k, '02b'): v / total for k, v in counts.items()}
