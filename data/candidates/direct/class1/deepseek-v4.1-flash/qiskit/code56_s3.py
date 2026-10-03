# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def not_gate(a):
    a = a & 0xFF
    qc = QuantumCircuit(8, 8)
    
    # Prepare the input state |a>
    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)
    
    # Apply bitwise NOT
    for i in range(8):
        qc.x(i)
    
    # Measure all qubits
    for i in range(8):
        qc.measure(i, i)
    
    # Simulate and sample
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts(qc)
    
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
