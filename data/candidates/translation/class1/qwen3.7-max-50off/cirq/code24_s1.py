# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    if isinstance(oracle, cirq.Circuit):
        n = len(oracle.all_qubits())
        qubits = cirq.LineQubit.range(n)
        qubit_map = dict(zip(sorted(oracle.all_qubits()), qubits))
        oracle_circuit = oracle.transform_qubits(lambda q: qubit_map[q])
    elif isinstance(oracle, cirq.Gate):
        n = oracle.num_qubits()
        qubits = cirq.LineQubit.range(n)
        oracle_circuit = cirq.Circuit(oracle.on(*qubits))
    elif isinstance(oracle, cirq.Operation):
        qubits = list(oracle.qubits)
        n = len(qubits)
        oracle_circuit = cirq.Circuit(oracle)
    else:
        n = getattr(oracle, 'num_qubits', None)
        if callable(n): 
            n = n()
        if n is None:
            n = len(oracle.qubits)
            qubits = list(oracle.qubits)
            oracle_circuit = cirq.Circuit(oracle)
        else:
            qubits = cirq.LineQubit.range(n)
            oracle_circuit = cirq.Circuit(oracle.on(*qubits))

    circuit_no_measure = cirq.Circuit()
    circuit_no_measure.append(cirq.X(qubits[n-1]))
    circuit_no_measure.append(cirq.H.on_each(*qubits))
    circuit_no_measure.append(oracle_circuit)
    circuit_no_measure.append(cirq.H.on_each(*qubits))
    
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit_no_measure, qubit_order=qubits)
    state_vector = result.final_state_vector
    
    probs = np.abs(state_vector)**2
    probs = probs.reshape((2**(n-1), 2))
    marginal_probs = np.sum(probs, axis=1)
    
    dist = {}
    for i in range(2**(n-1)):
        if marginal_probs[i] > 1e-9:
            bitstring = format(i, f'0{n-1}b')[::-1]
            dist[bitstring] = float(marginal_probs[i])
            
    total = sum(dist.values())
    if total > 0:
        dist = {k: v / total for k, v in dist.items()}
        
    return dist
