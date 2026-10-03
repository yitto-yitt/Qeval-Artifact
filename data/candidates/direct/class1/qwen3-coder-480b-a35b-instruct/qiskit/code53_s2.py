# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator

def xor_gate(a, b):
    # Create quantum registers for input bits and output bit
    qr = QuantumRegister(3)  # 3 qubits: a, b, result
    cr = ClassicalRegister(1)  # 1 classical register to store result
    qc = QuantumCircuit(qr, cr)

    # Initialize qubits based on input bits (a and b)
    if a & 1:  # If least significant bit of a is 1
        qc.x(0)  # Apply X gate to first qubit
    if b & 1:  # If least significant bit of b is 1
        qc.x(1)  # Apply X gate to second qubit

    # Perform XOR operation using CNOT gates
    qc.cx(0, 2)  # CNOT with control qubit 0 and target qubit 2
    qc.cx(1, 2)  # CNOT with control qubit 1 and target qubit 2

    # Measure the result qubit
    qc.measure(qr[2], cr[0])

    # Simulate the circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probabilities
    total_shots = sum(counts.values())
    prob_dist = {key.zfill(8): count / total_shots for key, count in counts.items()}

    # Pad all keys to 8 bits
    padded_prob_dist = {}
    for key, value in prob_dist.items():
        padded_key = key[-1].zfill(8)  # Take the last character and pad to 8 bits
        if len(key) == 1:  # If it's just a single bit result
            final_key = key + '0' * 7  # Pad with 7 zeros
        else:
            final_key = key.zfill(8)
        padded_prob_dist[final_key] = value

    # Ensure we have all 8-bit strings with 0 probability if not measured
    all_8bit_keys = [format(i, '08b') for i in range(256)]
    for key in all_8bit_keys:
        if key not in padded_prob_dist:
            padded_prob_dist[key] = 0.0

    return padded_prob_dist
