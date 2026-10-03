# EVAL_META: task_id=53, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def xor_gate(a: int, b: int) -> dict:
    """
    Design a quantum circuit that acts as a classical XOR gate on two 8-bit integers
    and sample the output. Returns a probability distribution dict.
    """
    qc = QuantumCircuit(8, 8)
    for i in range(8):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        if bit_a:
            qc.x(i)
        if bit_b:
            qc.x(i)
        qc.measure(i, i)
        
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    total_shots = sum(counts.values())
    probs = {state: count / total_shots for state, count in counts.items()}
    return probs
