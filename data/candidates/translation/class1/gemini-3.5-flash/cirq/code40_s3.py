# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

class StatePrepGate(cirq.Gate):
    def __init__(self, unitary):
        super().__init__()
        self.unitary = unitary
        
    def _num_qubits_(self) -> int:
        return 3
        
    def _unitary_(self):
        return self.unitary
        
    def _circuit_diagram_info_(self, args):
        return ["StatePrep"] * 3

def init_random_3qubit(desired_vector):
    # Ensure desired_vector is a normalized numpy array
    v = np.array(desired_vector, dtype=complex)
    v = v / np.linalg.norm(v)
    
    # Build a unitary matrix where the first column is v
    dim = len(v)
    rng = np.random.default_rng(42)
    A = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    A[:, 0] = v
    Q, _ = np.linalg.qr(A)
    Q[:, 0] = v
    
    # Create qubits and circuit
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(StatePrepGate(Q).on(*qubits))
    circuit.append(cirq.measure(*qubits, key='meas'))
    
    # Simulate
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    
    # Convert measurements to bitstrings and compute probabilities
    measurements = result.measurements['meas']
    counts = {}
    for row in measurements:
        bitstring = "".join(str(b) for b in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
