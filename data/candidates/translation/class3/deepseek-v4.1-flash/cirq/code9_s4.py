# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    params = [sympy.Symbol(f'theta_{i}') for i in range(12)]
    
    # Initial rotation layer
    for i, q in enumerate(qubits):
        circuit.append(cirq.ry(params[2*i])(q))
        circuit.append(cirq.rz(params[2*i+1])(q))
    circuit.append(cirq.barrier(*qubits))
    
    # Entanglement layer (full)
    for i in range(3):
        for j in range(i+1, 3):
            circuit.append(cirq.CX(qubits[i], qubits[j]))
    circuit.append(cirq.barrier(*qubits))
    
    # Final rotation layer
    for i, q in enumerate(qubits):
        circuit.append(cirq.ry(params[6 + 2*i])(q))
        circuit.append(cirq.rz(params[6 + 2*i+1])(q))
    circuit.append(cirq.barrier(*qubits))
    
    return circuit
