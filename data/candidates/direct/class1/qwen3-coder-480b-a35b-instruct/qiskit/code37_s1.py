# EVAL_META: task_id=37, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def bv_algorithm(s):
    n = len(s)
    
    # Create quantum circuit with n qubits for input register and 1 ancilla qubit
    qc = QuantumCircuit(n + 1, n)
    
    # Apply X gate to ancilla qubit (qubit n)
    qc.x(n)
    
    # Apply Hadamard gates to all qubits
    for i in range(n + 1):
        qc.h(i)
    
    # Apply oracle: CZ gates based on secret string s
    for i in range(n):
        if s[i] == '1':
            qc.cz(i, n)
    
    # Apply Hadamard gates to input register qubits
    for i in range(n):
        qc.h(i)
    
    # Measure input register qubits
    for i in range(n):
        qc.measure(i, i)
    
    # Run with Sampler using Aer simulator
    backend = AerSimulator()
    sampler = Sampler(backend)
    job = sampler.run([qc], shots=1000)
    result = job.result()
    
    # Extract bitstrings from results
    counts = result.quasi_dists[0]
    bitstrings = list(counts.keys())
    
    # Convert bitstrings to binary strings
    bitstrings = [format(bitstring, f'0{n}b') for bitstring in bitstrings]
    
    return [bitstrings, result]
