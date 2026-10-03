# EVAL_META: task_id=55, framework=cirq, class=1
import cirq

def or_gate(a, b):
    q = cirq.LineQubit.range(9)
    a_qubits = q[0:3]
    b_qubits = q[3:6]
    c_qubits = q[6:9]
    
    circuit = cirq.Circuit()
    
    for i in range(3):
        if (a >> i) & 1:
            circuit.append(cirq.X(a_qubits[i]))
        if (b >> i) & 1:
            circuit.append(cirq.X(b_qubits[i]))
    
    for i in range(3):
        circuit.append(cirq.CNOT(a_qubits[i], c_qubits[i]))
        circuit.append(cirq.CNOT(b_qubits[i], c_qubits[i]))
        circuit.append(cirq.TOFFOLI(a_qubits[i], b_qubits[i], c_qubits[i]))
    
    circuit.append(cirq.measure(*c_qubits, key='result'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='result')
    total = sum(counts.values())
    
    return {format(outcome, '03b'): count / total for outcome, count in counts.items()}
