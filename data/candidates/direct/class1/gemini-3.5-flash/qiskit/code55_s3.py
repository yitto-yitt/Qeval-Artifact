# EVAL_META: task_id=55, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def or_gate(a: int, b: int) -> dict:
    # 3 qubits for a (0,1,2), 3 for b (3,4,5), 3 for result c (6,7,8)
    qc = QuantumCircuit(9, 3)
    
    for i in range(3):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        
        if bit_a:
            qc.x(i)
        if bit_b:
            qc.x(i + 3)
            
        # OR gate: c_i = a_i OR b_i
        # Implemented as: c_i = a_i ^ b_i ^ (a_i & b_i)
        qc.cx(i, i + 6)
        qc.cx(i + 3, i + 6)
        qc.ccx(i, i + 3, i + 6)
        
        qc.measure(i + 6, i)
        
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    counts = job.result().get_counts()
    
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    return probabilities
