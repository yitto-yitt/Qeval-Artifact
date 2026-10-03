# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator

def and_gate(a, b):
    # Create quantum registers for input bits (a and b) and output bits
    qr = QuantumRegister(6)  # 3 bits for a, 3 bits for b
    cr = ClassicalRegister(3)  # 3 bits for output of AND operation
    qc = QuantumCircuit(qr, cr)

    # Encode input a into first 3 qubits
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)  # Apply X gate to set bit to 1
    
    # Encode input b into next 3 qubits
    for i in range(3):
        if (b >> i) & 1:
            qc.x(i + 3)  # Apply X gate to set bit to 1

    # Perform bitwise AND operation using CNOT gates with ancilla qubits
    # Ancilla qubits will store the result
    for i in range(3):
        qc.ccx(i, i+3, i+6)  # Controlled-controlled-X (Toffoli gate) for AND operation
        qc.measure(i+6, i)   # Measure the result qubit

    # Execute the circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts(qc)
    
    # Convert counts to probabilities
    total_shots = sum(counts.values())
    prob_dist = {key: count / total_shots for key, count in counts.items()}
    
    return prob_dist
