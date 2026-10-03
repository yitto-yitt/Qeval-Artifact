# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    params = sympy.symbols('theta_0:12')
    idx = 0
    
    for q in qubits:
        circuit.append(cirq.ry(params[idx]).on(q))
        circuit.append(cirq.rz(params[idx+1]).on(q))
        idx += 2
        
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.CNOT(qubits[1], qubits[2]))
    
    for q in qubits:
        circuit.append(cirq.ry(params[idx]).on(q))
        circuit.append(cirq.rz(params[idx+1]).on(q))
        idx += 2
        
    return circuit
