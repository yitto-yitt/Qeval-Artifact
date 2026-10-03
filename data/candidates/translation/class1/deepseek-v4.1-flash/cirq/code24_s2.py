# EVAL_META: task_id=24, framework=cirq, class=1
import cirq

def dj_algorithm(oracle):
    qubits = sorted(oracle.all_qubits())
    n = len(qubits)
    input_qubits = qubits[:-1]
    output_qubit = qubits[-1]
    
    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(oracle)
    circuit.append(cirq.H(q) for q in qubits)
    
    qubit_order = [output_qubit] + list(reversed(input_qubits))
    state = cirq.final_state_vector(circuit, qubit_order=qubit_order)
    
    probs = {}
    for i in range(2**(n-1)):
        prob = 0.0
        for out in range(2):
            index = (out << (n-1)) + i
            prob += abs(state[index])**2
        if prob > 1e-12:
            key = format(i, f'0{n-1}b')
            probs[key] = prob
    return probs
