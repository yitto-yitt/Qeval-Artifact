# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    # Layer 0 rotations
    for i in range(3):
        circuit.append(cirq.ry(sympy.Symbol(f'θ[{2*i}]'))(qubits[i]))
        circuit.append(cirq.rz(sympy.Symbol(f'θ[{2*i+1}]'))(qubits[i]))
        
    # Barrier
    circuit.append(cirq.Barrier(3).on(*qubits))
    
    # Entanglement layer (reverse_linear)
    circuit.append(cirq.CNOT(qubits[2], qubits[1]))
    circuit.append(cirq.CNOT(qubits[1], qubits[0]))
    
    # Barrier
    circuit.append(cirq.Barrier(3).on(*qubits))
    
    # Layer 1 rotations
    for i in range(3):
        circuit.append(cirq.ry(sympy.Symbol(f'θ[{2*i+6}]'))(qubits[i]))
        circuit.append(cirq.rz(sympy.Symbol(f'θ[{2*i+7}]'))(qubits[i]))
        
    return circuit
