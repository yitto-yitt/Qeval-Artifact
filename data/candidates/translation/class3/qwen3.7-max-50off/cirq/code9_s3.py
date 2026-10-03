# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    params = [sympy.Symbol(f'θ[{i}]') for i in range(12)]
    
    circuit.append([
        cirq.ry(params[0]).on(qubits[0]),
        cirq.rz(params[1]).on(qubits[0]),
        cirq.ry(params[2]).on(qubits[1]),
        cirq.rz(params[3]).on(qubits[1]),
        cirq.ry(params[4]).on(qubits[2]),
        cirq.rz(params[5]).on(qubits[2]),
    ])
    
    circuit.append(cirq.CNOT(qubits[2], qubits[1]))
    circuit.append(cirq.CNOT(qubits[1], qubits[0]))
    
    circuit.append([
        cirq.ry(params[6]).on(qubits[0]),
        cirq.rz(params[7]).on(qubits[0]),
        cirq.ry(params[8]).on(qubits[1]),
        cirq.rz(params[9]).on(qubits[1]),
        cirq.ry(params[10]).on(qubits[2]),
        cirq.rz(params[11]).on(qubits[2]),
    ])
    
    return circuit
