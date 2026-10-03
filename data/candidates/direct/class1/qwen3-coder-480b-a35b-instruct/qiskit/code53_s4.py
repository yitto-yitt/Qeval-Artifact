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

    return prob_dist
