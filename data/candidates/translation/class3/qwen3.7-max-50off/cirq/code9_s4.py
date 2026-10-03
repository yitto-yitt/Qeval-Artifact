# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    params = [sympy.Symbol(f'p_{i}') for i in range(12)]
    
    for i in range(3):
        circuit.append(cirq.ry(params[2*i]).on(qubits[i]))
        circuit.append(cirq.rz(params[2*i+1]).on(qubits[i]))
        
    circuit.append(cirq.CNOT(qubits[1], qubits[0]))
    circuit.append(cirq.CNOT(qubits[2], qubits[1]))
    
    for i in range(3):
        circuit.append(cirq.ry(params[6+2*i]).on(qubits[i]))
        circuit.append(cirq.rz(params[6+2*i+1]).on(qubits[i]))
        
    return circuit
