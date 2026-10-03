# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator

def and_gate(a, b):
    # Create quantum registers for input bits (a and b) and output bits
    qr = QuantumRegister(6)  # 3 bits for a, 3 bits for b
    cr = ClassicalRegister(3)  # 3 bits for output of AND operation
    qc = QuantumCircuit(qr, cr)

    # Encode input a and b into quantum states
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)  # Apply X gate to set bit to 1
        if (b >> i) & 1:
            qc.x(i + 3)  # Apply X gate to set bit to 1

    # Perform AND operation using CNOT gates controlled on each pair of bits
    # The result will be stored in ancilla qubits which we'll measure
    ancilla_qubits = [6 + i for i in range(3)]
    
    # Add ancilla qubits to the circuit
    qc.add_register(QuantumRegister(3))  # Adding 3 more qubits for results
    
    # Perform AND operations for each bit position
    for i in range(3):
        qc.ccx(i, i+3, i+6)  # CCX (Toffoli) gate: |a_i>|b_i>|0> -> |a_i>|b_i>|a_i AND b_i>
        
    # Measure the result qubits
    for i in range(3):
        qc.measure(i+6, i)

    # Simulate the circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probabilities
    total_shots = sum(counts.values())
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    
    return prob_dist
