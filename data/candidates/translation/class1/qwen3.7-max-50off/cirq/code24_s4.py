# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    if isinstance(oracle, cirq.Circuit):
        qubits = sorted(oracle.all_qubits())
        n = len(qubits)
    elif hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits()
        qubits = cirq.LineQubit.range(n)
    else:
        raise ValueError("Unsupported oracle type")

    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[n-1]))
    circuit.append(cirq.H.on_each(*qubits))
    
    if isinstance(oracle, cirq.Circuit):
        circuit.append(oracle)
    else:
        circuit.append(oracle.on(*qubits))
        
    circuit.append(cirq.H.on_each(*qubits))
    
    input_qubits = qubits[:n-1]
    if n > 1:
        circuit.append(cirq.measure(*input_qubits, key='m'))
    
    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    state_vector = result.final_state_vector
    
    probs = np.abs(state_vector)**2
    probs = probs.reshape([2]*n)
    probs_marginal = np.sum(probs, axis=-1)
    
    dist = {}
    for i in range(2**(n-1)):
        bitstring = format(i, f'0{n-1}b')
        prob = probs_marginal.flatten()[i]
        if prob > 1e-9:
            dist[bitstring] = float(prob)
            
    total = sum(dist.values())
    if total > 0:
        dist = {k: v / total for k, v in dist.items()}
        
    return dist
