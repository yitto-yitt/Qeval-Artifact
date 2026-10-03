# EVAL_META: task_id=40, framework=cirq, class=1
import numpy as np
import cirq

def init_random_3qubit(desired_vector):
    vec = np.array(desired_vector, dtype=np.complex128).flatten()
    vec = vec / np.linalg.norm(vec)
    n = len(vec)
    
    basis = [vec]
    for i in range(n):
        e = np.zeros(n, dtype=np.complex128)
        e[i] = 1.0
        basis.append(e)
        
    U = np.zeros((n, n), dtype=np.complex128)
    idx = 0
    for b in basis:
        if idx >= n:
            break
        v = b.copy()
        for j in range(idx):
            v -= np.dot(np.conj(U[:, j]), b) * U[:, j]
        norm = np.linalg.norm(v)
        if norm > 1e-10:
            U[:, idx] = v / norm
            idx += 1
            
    qubits = cirq.LineQubit.range(3)
    gate = cirq.MatrixGate(U)
    circuit = cirq.Circuit(gate.on(qubits[2], qubits[1], qubits[0]))
    circuit.append(cirq.measure(qubits[2], qubits[1], qubits[0], key='meas'))
    
    sim = cirq.Simulator(seed=42)
    result = sim.run(circuit, repetitions=1000)
    counts = result.histogram(key='meas')
    
    total = sum(counts.values())
    return {f"{k:03b}": v / total for k, v in counts.items()}
