# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    # Create quantum registers for input bits and output bit
    qr = QuantumRegister(3)  # 3 qubits: a, b, result
    cr = ClassicalRegister(1)  # 1 classical register to store result
    qc = QuantumCircuit(qr, cr)

    # Set input qubits based on a and b (only consider least significant bit for simplicity)
    if a & 1:  # If least significant bit of a is 1
        qc.x(0)  # Apply X gate to first qubit
    if b & 1:  # If least significant bit of b is 1
        qc.x(1)  # Apply X gate to second qubit

    # Perform XOR operation using CNOT gates
    qc.cx(0, 2)  # Control from qubit 0 (a), target qubit 2 (result)
    qc.cx(1, 2)  # Control from qubit 1 (b), target qubit 2 (result)

    # Measure the result qubit
    qc.measure(qr[2], cr[0])

    # Simulate the circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts(qc)

    # Convert counts to 8-bit string format
    final_counts = {}
    for outcome, count in counts.items():
        # Pad the outcome to 8 bits with leading zeros
        padded_outcome = outcome.zfill(8)
        final_counts[padded_outcome] = count

    return final_counts
