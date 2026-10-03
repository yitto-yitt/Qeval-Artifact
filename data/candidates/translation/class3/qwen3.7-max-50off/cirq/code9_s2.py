# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    params = sympy.symbols('theta_0:12')
    
    for i in range(3):
        circuit.append(cirq.ry(params[i]).on(qubits[i]))
    for i in range(3):
        circuit.append(cirq.rz(params[i+3]).on(qubits[i]))
    circuit.append(cirq.Barrier(3).on(*qubits))
    
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.CNOT(qubits[1], qubits[2]))
    circuit.append(cirq.Barrier(3).on(*qubits))
    
    for i in range(3):
        circuit.append(cirq.ry(params[i+6]).on(qubits[i]))
    for i in range(3):
        circuit.append(cirq.rz(params[i+9]).on(qubits[i]))
    circuit.append(cirq.Barrier(3).on(*qubits))
    
    return circuit
