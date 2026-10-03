# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    # Create quantum registers for input bits and output bit
    qr = QuantumRegister(3)  # 3 qubits: a, b, result
    cr = ClassicalRegister(1)  # 1 classical register to store result
    qc = QuantumCircuit(qr, cr)

    # Set input qubits based on a and b (only consider least significant bit for XOR)
    if a & 1:  # If least significant bit of a is 1
        qc.x(0)  # Apply X gate to first qubit
    if b & 1:  # If least significant bit of b is 1
        qc.x(1)  # Apply X gate to second qubit

    # Apply CNOT gates to perform XOR operation
    # XOR is implemented using CNOT gate where control is one input and target is the ancilla
    qc.cx(0, 2)  # CNOT with first qubit as control and third as target
    qc.cx(1, 2)  # CNOT with second qubit as control and third as target

    # Measure the result qubit
    qc.measure(qr[2], cr[0])

    # Simulate the circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Format the output to match 8-bit requirement
    formatted_counts = {}
    for key, value in counts.items():
        # Pad the binary string to 8 bits
        padded_key = key.zfill(8)
        formatted_counts[padded_key] = value

    return formatted_counts
