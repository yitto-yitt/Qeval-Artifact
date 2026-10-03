# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit import transpile

def and_gate(a, b):
    # Create quantum registers for input a, input b, and output
    qr_a = QuantumRegister(3, 'a')
    qr_b = QuantumRegister(3, 'b')
    qr_out = QuantumRegister(3, 'out')
    cr_out = ClassicalRegister(3, 'c')
    
    # Create quantum circuit
    qc = QuantumCircuit(qr_a, qr_b, qr_out, cr_out)
    
    # Encode integer a into qubits
    for i in range(3):
        if (a >> i) & 1:
            qc.x(qr_a[i])
    
    # Encode integer b into qubits
    for i in range(3):
        if (b >> i) & 1:
            qc.x(qr_b[i])
    
    # Apply AND operation using Toffoli gates (CCX)
    for i in range(3):
        qc.ccx(qr_a[i], qr_b[i], qr_out[i])
    
    # Measure output qubits
    for i in range(3):
        qc.measure(qr_out[i], cr_out[i])
    
    # Simulate the circuit
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=1000).result()
    counts = result.get_counts(qc)
    
    # Convert counts to probability distribution
    total_shots = sum(counts.values())
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    
    return prob_dist
