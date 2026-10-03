# EVAL_META: task_id=24, framework=cirq, class=1
import cirq

def dj_algorithm(oracle):
    if isinstance(oracle, cirq.Circuit):
        qubits = sorted(oracle.all_qubits())
        n = len(qubits)
    elif isinstance(oracle, cirq.Gate):
        n = oracle.num_qubits()
        qubits = cirq.LineQubit.range(n)
    else:
        n = getattr(oracle, 'num_qubits', None)
        if n is None:
            n = len(oracle.all_qubits())
            qubits = sorted(oracle.all_qubits())
        else:
            if callable(n):
                n = n()
            qubits = cirq.LineQubit.range(n)
            
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[n - 1]))
    circuit.append(cirq.H(q) for q in qubits)
    
    if isinstance(oracle, cirq.Gate):
        circuit.append(oracle(*qubits))
    elif isinstance(oracle, cirq.Circuit):
        circuit.append(oracle)
    else:
        circuit.append(oracle(*qubits))
        
    circuit.append(cirq.H(q) for q in qubits)
    
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    state_vector = result.final_state_vector
    
    probs = {}
    num_states = 2**n
    for i in range(num_states):
        input_val = i >> 1
        bs = format(input_val, f'0{n-1}b')[::-1]
        prob = abs(state_vector[i])**2
        if bs in probs:
            probs[bs] += prob
        else:
            probs[bs] = prob
            
    probs = {k: v for k, v in probs.items() if v > 1e-10}
    total = sum(probs.values())
    if total > 0:
        probs = {k: v / total for k, v in probs.items()}
        
    return probs
