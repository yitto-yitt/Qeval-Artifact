# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2() -> cirq.Circuit:
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    # Layer 0 rotations
    circuit.append([
        cirq.ry(sympy.Symbol('θ[0]'))(qubits[0]),
        cirq.rz(sympy.Symbol('θ[1]'))(qubits[0]),
        cirq.ry(sympy.Symbol('θ[2]'))(qubits[1]),
        cirq.rz(sympy.Symbol('θ[3]'))(qubits[1]),
        cirq.ry(sympy.Symbol('θ[4]'))(qubits[2]),
        cirq.rz(sympy.Symbol('θ[5]'))(qubits[2]),
    ])
    
    # Barrier
    circuit.append(cirq.Barrier(3).on(*qubits))
    
    # Entanglement layer (reverse_linear: (2, 1), (1, 0))
    circuit.append([
        cirq.CNOT(qubits[2], qubits[1]),
        cirq.CNOT(qubits[1], qubits[0])
    ])
    
    # Barrier
    circuit.append(cirq.Barrier(3).on(*qubits))
    
    # Layer 1 rotations
    circuit.append([
        cirq.ry(sympy.Symbol('θ[6]'))(qubits[0]),
        cirq.rz(sympy.Symbol('θ[7]'))(qubits[0]),
        cirq.ry(sympy.Symbol('θ[8]'))(qubits[1]),
        cirq.rz(sympy.Symbol('θ[9]'))(qubits[1]),
        cirq.ry(sympy.Symbol('θ[10]'))(qubits[2]),
        cirq.rz(sympy.Symbol('θ[11]'))(qubits[2]),
    ])
    
    return circuit
