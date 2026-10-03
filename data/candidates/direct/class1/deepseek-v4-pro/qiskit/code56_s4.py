# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def not_gate(a):
    qc = QuantumCircuit(8, 8)
    
    # Prepare the input state corresponding to integer a
    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)
    
    # Apply bitwise NOT to all 8 qubits
    for i in range(8):
        qc.x(i)
    
    qc.measure(range(8), range(8))
    
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts(qc)
    total_shots = sum(counts.values())
    
    return {bitstring: count / total_shots for bitstring, count in counts.items()}
