# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    
    # Build Bell circuit
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    
    # Add noise: depolarizing after gates and bit flip before measurement
    noisy_circuit = cirq.Circuit()
    for op in circuit.all_operations():
        noisy_circuit.append(op)
        if len(op.qubits) == 1:
            noisy_circuit.append(cirq.depolarize(0.001).on(op.qubits[0]))
        elif len(op.qubits) == 2:
            for q in op.qubits:
                noisy_circuit.append(cirq.depolarize(0.01).on(q))
    
    noisy_circuit.append(cirq.bit_flip(0.02).on(q0))
    noisy_circuit.append(cirq.bit_flip(0.02).on(q1))
    noisy_circuit.append(cirq.measure(q0, q1, key='m'))
    
    # Simulate
    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    counts = result.histogram(key='m')
    total = sum(counts.values())
    
    # Convert to bitstring probabilities (Qiskit convention: q0 is least significant bit)
    probs = {format(k, '02b'): v / total for k, v in counts.items()}
    return probs
