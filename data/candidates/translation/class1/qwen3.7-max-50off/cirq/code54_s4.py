# EVAL_META: task_id=54, framework=cirq, class=1
import cirq

def and_gate(a, b):
    a_qubits = cirq.LineQubit.range(0, 3)
    b_qubits = cirq.LineQubit.range(3, 6)
    anc_qubits = cirq.LineQubit.range(6, 9)
    
    circuit = cirq.Circuit()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '1':
            circuit.append(cirq.X(a_qubits[i]))
        if b_bin[2-i] == '1':
            circuit.append(cirq.X(b_qubits[i]))
            
    for i in range(3):
        circuit.append(cirq.CCX(a_qubits[i], b_qubits[i], anc_qubits[i]))
        
    circuit.append(cirq.measure(*anc_qubits, key='measure'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    
    counts = {}
    for row in result.measurements['measure']:
        bitstring = f"{row[2]}{row[1]}{row[0]}"
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
