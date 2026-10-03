# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(cirq.measure(*qubits, key='m'))
    
    initial_state = np.array(desired_vector, dtype=np.complex128)
    
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024, initial_state=initial_state)
    
    counts = {}
    for row in result.measurements['m']:
        bitstring = f"{row[2]}{row[1]}{row[0]}"
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
