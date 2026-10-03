# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    
    theta = [sympy.Symbol(f'θ[{i}]') for i in range(6)]
    phi = [sympy.Symbol(f'φ[{i}]') for i in range(6)]
    
    moments = []
    # RY layer 1
    moments.append(cirq.Moment([cirq.ry(theta[0]).on(qubits[0]),
                                cirq.ry(theta[1]).on(qubits[1]),
                                cirq.ry(theta[2]).on(qubits[2])]))
    # RZ layer 1
    moments.append(cirq.Moment([cirq.rz(phi[0]).on(qubits[0]),
                                cirq.rz(phi[1]).on(qubits[1]),
                                cirq.rz(phi[2]).on(qubits[2])]))
    # Entanglement (CX linear)
    moments.append(cirq.Moment([cirq.CX(qubits[0], qubits[1]),
                                cirq.CX(qubits[1], qubits[2])]))
    # RY layer 2
    moments.append(cirq.Moment([cirq.ry(theta[3]).on(qubits[0]),
                                cirq.ry(theta[4]).on(qubits[1]),
                                cirq.ry(theta[5]).on(qubits[2])]))
    # RZ layer 2
    moments.append(cirq.Moment([cirq.rz(phi[3]).on(qubits[0]),
                                cirq.rz(phi[4]).on(qubits[1]),
                                cirq.rz(phi[5]).on(qubits[2])]))
    
    return cirq.Circuit(moments)
