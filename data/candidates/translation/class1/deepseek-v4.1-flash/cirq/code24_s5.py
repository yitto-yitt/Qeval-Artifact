# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    if hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits() if callable(oracle.num_qubits) else oracle.num_qubits
    elif isinstance(oracle, cirq.Operation):
        n = len(oracle.qubits)
    elif isinstance(oracle, cirq.Circuit):
        n = len(oracle.all_qubits())
    else:
        n = cirq.num_qubits(oracle)
    
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    circuit.append(cirq.X(qubits[-1]))
    circuit.append(cirq.H.on_each(*qubits))
    
    if isinstance(oracle, cirq.Gate):
        circuit.append(oracle.on(*qubits))
    elif isinstance(oracle, cirq.Circuit):
        mapping = {q: qubits[i] for i, q in enumerate(sorted(oracle.all_qubits()))}
        circuit.append(oracle.transform_qubits(mapping))
    elif isinstance(oracle, cirq.Operation):
        if isinstance(oracle, cirq.CircuitOperation):
            circ = cirq.Circuit(oracle.circuit)
            mapping = {q: qubits[i] for i, q in enumerate(sorted(circ.all_qubits()))}
            circuit.append(circ.transform_qubits(mapping))
        else:
            circuit.append(oracle.gate.on(*qubits))
    else:
        circuit.append(oracle.on(*qubits))
    
    circuit.append(cirq.H.on_each(*qubits))
    
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    state = result.final_state_vector
    
    probs = {}
    for i in range(2**n):
        prob = abs(state[i])**2
        if prob < 1e-12:
            continue
        input_val = i >> 1
        key = format(input_val, f'0{n-1}b')[::-1] if n > 1 else ''
        probs[key] = probs.get(key, 0.0) + prob
    
    total = sum(probs.values())
    if total > 0:
        probs = {k: v / total for k, v in probs.items()}
    return probs
