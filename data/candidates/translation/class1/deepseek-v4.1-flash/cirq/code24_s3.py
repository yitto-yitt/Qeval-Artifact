# EVAL_META: task_id=24, framework=cirq, class=1
import cirq

def dj_algorithm(oracle):
    n = len(oracle.all_qubits())
    old_qubits = sorted(oracle.all_qubits())
    qubits = cirq.LineQubit.range(n)
    mapping = {old: new for old, new in zip(old_qubits, qubits)}
    mapped_oracle = oracle.transform_qubits(mapping)
    
    input_qubits = qubits[:-1]
    output_qubit = qubits[-1]
    
    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(mapped_oracle)
    circuit.append(cirq.H.on_each(*qubits))
    
    state = cirq.final_state_vector(circuit, qubit_order=qubits)
    
    probs = {}
    for i, amp in enumerate(state):
        prob = abs(amp) ** 2
        if prob < 1e-12:
            continue
        bits = format(i, f'0{n}b')
        input_bits_cirq = bits[:n-1]
        key = input_bits_cirq[::-1]
        probs[key] = probs.get(key, 0.0) + prob
    return probs
