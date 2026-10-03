# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    # 12 parameters for 3 qubits, reps=1 (2 rotation layers, 6 parameters each)
    theta = [sympy.Symbol(f'θ[{i}]') for i in range(12)]
    
    # Rotation layer 0
    for i in range(3):
        circuit.append(cirq.ry(theta[2*i])(qubits[i]))
        circuit.append(cirq.rz(theta[2*i+1])(qubits[i]))
        
    # Barrier
    circuit.append(cirq.barrier(*qubits))
    
    # Entanglement layer 0 (reverse_linear)
    circuit.append(cirq.CNOT(qubits[2], qubits[1]))
    circuit.append(cirq.CNOT(qubits[1], qubits[0]))
    
    # Barrier
    circuit.append(cirq.barrier(*qubits))
    
    # Rotation layer 1
    for i in range(3):
        circuit.append(cirq.ry(theta[6 + 2*i])(qubits[i]))
        circuit.append(cirq.rz(theta[6 + 2*i+1])(qubits[i]))
        
    return circuit
