# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator

def and_gate(a, b):
    # Create quantum registers for input bits (a and b) and output bits
    qr = QuantumRegister(6)  # 3 bits for a, 3 bits for b
    cr = ClassicalRegister(3)  # 3 bits for output of AND operation
    qc = QuantumCircuit(qr, cr)

    # Encode input values a and b into quantum states
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)  # Apply X gate to set bit to 1
        if (b >> i) & 1:
            qc.x(i + 3)  # Apply X gate to set bit to 1

    # Perform bitwise AND operation using CNOT gates with ancilla qubits
    # We'll use the first 6 qubits for inputs and compute AND on classical register
    for i in range(3):
        # Use controlled-X (CNOT-like) where both control qubits must be 1 for output to be 1
        qc.ccx(i, i+3, i)  # Using the same qubit index might not work; let's use extra qubits
        # Actually, we need ancilla qubits for AND operations
        pass

    # Redefine circuit with enough qubits for ancillas
    qc = QuantumCircuit(9, 3)  # 3 for a, 3 for b, 3 ancillas for results
    
    # Encode inputs
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(i + 3)
    
    # Perform AND operations using CCX (Toffoli) gates
    for i in range(3):
        qc.ccx(i, i + 3, 6 + i)  # Ancilla qubits at positions 6, 7, 8
        qc.measure(6 + i, i)     # Measure result to classical register

    # Simulate the circuit
    backend = AerSimulator()
    job = backend.run(qc, shots=1024)
    counts = job.result().get_counts()

    # Calculate probabilities
    total_shots = sum(counts.values())
    prob_dist = {outcome: count / total_shots for outcome, count in counts.items()}
    
    return prob_dist
