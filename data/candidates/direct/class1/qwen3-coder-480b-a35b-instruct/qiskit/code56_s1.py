# EVAL_META: task_id=56, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

def not_gate(a):
    # Create quantum and classical registers
    qr = QuantumRegister(8)
    cr = ClassicalRegister(8)
    qc = QuantumCircuit(qr, cr)
    
    # Convert input to binary and apply X gates for 1s
    binary_str = format(a, '08b')
    for i in range(8):
        if binary_str[i] == '1':
            qc.x(i)
    
    # Apply NOT gate (X gate) to all qubits
    for i in range(8):
        qc.x(i)
    
    # Measure all qubits
    qc.measure(range(8), range(8))
    
    # Simulate the circuit
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1000)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    # Normalize to get probability distribution
    total_shots = sum(counts.values())
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    
    return prob_dist
