# EVAL_META: task_id=40, framework=cirq, class=1
import numpy as np
import cirq

def init_random_3qubit(desired_vector):
    v = np.array(desired_vector, dtype=complex)
    v = v / np.linalg.norm(v)
    n = len(v)
    
    # Construct a unitary matrix that maps |000> to the desired state (up to global phase)
    # using QR decomposition. The global phase does not affect measurement probabilities.
    rng = np.random.default_rng(42)
    mat = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    mat[:, 0] = v
    
    q, r = np.linalg.qr(mat)
    U = q
    
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.MatrixGate(U).on(*qubits),
        cirq.measure(*qubits, key='meas')
    )
    
    # Run the circuit on the simulator with the same seed and default shot count (4000)
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=4000)
    counts = result.histogram(key='meas')
    
    total = sum(counts.values())
    probs = {}
    for i, count in counts.items():
        # Cirq's histogram integer maps to binary with q0 as LSB, matching Qiskit's bitstring format
        bitstring = format(i, '03b')
        probs[bitstring] = count / total
        
    return probs
