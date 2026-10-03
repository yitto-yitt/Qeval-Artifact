# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    vec = np.array(desired_vector, dtype=np.complex128).flatten()
    vec = vec / np.linalg.norm(vec)
    
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(vec).on(*qubits))
    circuit.append(cirq.measure(*qubits, key='m'))
    
    sim = cirq.Simulator(seed=42)
    result = sim.run(circuit, repetitions=1024)
    counts = result.histogram(key='m')
    
    total = sum(counts.values())
    probs = {}
    for state, count in counts.items():
        # Cirq measures q0 as MSB, Qiskit formats bitstrings with q0 as LSB
        bitstring = format(state, '03b')[::-1]
        probs[bitstring] = count / total
        
    return probs
