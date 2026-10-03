# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    if hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits() if callable(oracle.num_qubits) else oracle.num_qubits
    else:
        n = len(oracle.all_qubits())
        
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    circuit.append(cirq.X(qubits[n-1]))
    circuit.append(cirq.H.on_each(*qubits))
    
    if isinstance(oracle, cirq.Circuit):
        circuit.append(oracle)
    elif isinstance(oracle, cirq.Gate):
        circuit.append(oracle.on(*qubits))
    elif isinstance(oracle, cirq.Operation):
        circuit.append(oracle)
    elif callable(oracle):
        circuit.append(oracle(*qubits))
    else:
        circuit.append(oracle)
        
    circuit.append(cirq.H.on_each(*qubits))
    
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    state_vector = result.final_state_vector
    
    probs = {}
    for i in range(2**(n-1)):
        prob = 0.0
        for j in range(2):
            idx = (i << 1) | j
            prob += abs(state_vector[idx])**2
        
        if prob > 1e-9:
            bitstring = format(i, f'0{n-1}b')[::-1]
            probs[bitstring] = prob
            
    return probs
