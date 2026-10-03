# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    theta = [sympy.Symbol(f'θ[{i}]') for i in range(12)]
    circuit = cirq.Circuit()
    
    # Initial rotation layer: RY then RZ
    circuit.append(cirq.Moment([cirq.ry(theta[0])(qubits[0]),
                                cirq.ry(theta[1])(qubits[1]),
                                cirq.ry(theta[2])(qubits[2])]))
    circuit.append(cirq.Moment([cirq.rz(theta[3])(qubits[0]),
                                cirq.rz(theta[4])(qubits[1]),
                                cirq.rz(theta[5])(qubits[2])]))
    
    # Entanglement layer: reverse_linear for 3 qubits -> CX(1,2) then CX(0,1)
    circuit.append(cirq.CX(qubits[1], qubits[2]))
    circuit.append(cirq.CX(qubits[0], qubits[1]))
    
    # Final rotation layer: RY then RZ
    circuit.append(cirq.Moment([cirq.ry(theta[6])(qubits[0]),
                                cirq.ry(theta[7])(qubits[1]),
                                cirq.ry(theta[8])(qubits[2])]))
    circuit.append(cirq.Moment([cirq.rz(theta[9])(qubits[0]),
                                cirq.rz(theta[10])(qubits[1]),
                                cirq.rz(theta[11])(qubits[2])]))
    
    return circuit
