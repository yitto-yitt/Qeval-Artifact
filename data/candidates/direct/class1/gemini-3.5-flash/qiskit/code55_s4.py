# EVAL_META: task_id=55, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def or_gate(a: int, b: int) -> dict:
    # We use 9 qubits:
    # 0, 1, 2 for a (LSB to MSB)
    # 3, 4, 5 for b (LSB to MSB)
    # 6, 7, 8 for the result c (LSB to MSB)
    qc = QuantumCircuit(9, 3)
    
    # Initialize input a
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
            
    # Initialize input b
    for i in range(3):
        if (b >> i) & 1:
            qc.x(3 + i)
            
    # Compute bitwise OR: c_i = a_i OR b_i
    # Using the logic: c_i = a_i ^ b_i ^ (a_i & b_i)
    for i in range(3):
        qc.cx(i, 6 + i)
        qc.cx(3 + i, 6 + i)
        qc.ccx(i, 3 + i, 6 + i)
        
    # Measure result c into classical bits
    # c_0 (qubit 6) -> clbit 0
    # c_1 (qubit 7) -> clbit 1
    # c_2 (qubit 8) -> clbit 2
    for i in range(3):
        qc.measure(6 + i, i)
        
    # Run simulation
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Normalize counts to probabilities
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    
    return probabilities
