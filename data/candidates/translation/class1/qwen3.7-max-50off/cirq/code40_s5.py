# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    vec = np.array(desired_vector, dtype=np.complex128)
    vec = vec / np.linalg.norm(vec)
    
    state_prep = cirq.StatePreparationChannel(vec)
    circuit.append(state_prep.on(*qubits[::-1]))
    circuit.append(cirq.measure(*qubits[::-1], key='m'))
    
    sim = cirq.Simulator(seed=42)
    result = sim.run(circuit, repetitions=1000)
    
    hist = result.histogram(key='m')
    total = sum(hist.values())
    
    return {format(i, '03b'): count / total for i, count in hist.items()}
