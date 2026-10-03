# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    theta = [sympy.Symbol(f"θ[{i}]") for i in range(12)]

    circuit = cirq.Circuit()
    circuit.append([cirq.ry(theta[i]).on(qubits[i]) for i in range(3)])
    circuit.append([cirq.rz(theta[i + 3]).on(qubits[i]) for i in range(3)])
    circuit.append(cirq.BarrierGate(3).on(*qubits))
    circuit.append([cirq.CNOT(qubits[1], qubits[2]), cirq.CNOT(qubits[0], qubits[1])])
    circuit.append(cirq.BarrierGate(3).on(*qubits))
    circuit.append([cirq.ry(theta[i + 6]).on(qubits[i]) for i in range(3)])
    circuit.append([cirq.rz(theta[i + 9]).on(qubits[i]) for i in range(3)])

    return circuit
