# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    theta = [sympy.Symbol(f"θ[{i}]") for i in range(12)]

    circuit = cirq.Circuit()

    circuit.append(cirq.ry(theta[0]).on(qubits[0]))
    circuit.append(cirq.ry(theta[1]).on(qubits[1]))
    circuit.append(cirq.ry(theta[2]).on(qubits[2]))
    circuit.append(cirq.rz(theta[3]).on(qubits[0]))
    circuit.append(cirq.rz(theta[4]).on(qubits[1]))
    circuit.append(cirq.rz(theta[5]).on(qubits[2]))

    if hasattr(cirq, "barrier"):
        circuit.append(cirq.barrier(*qubits))
    elif hasattr(cirq, "BarrierGate"):
        circuit.append(cirq.BarrierGate(3).on(*qubits))

    circuit.append(cirq.CNOT(qubits[1], qubits[2]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))

    if hasattr(cirq, "barrier"):
        circuit.append(cirq.barrier(*qubits))
    elif hasattr(cirq, "BarrierGate"):
        circuit.append(cirq.BarrierGate(3).on(*qubits))

    circuit.append(cirq.ry(theta[6]).on(qubits[0]))
    circuit.append(cirq.ry(theta[7]).on(qubits[1]))
    circuit.append(cirq.ry(theta[8]).on(qubits[2]))
    circuit.append(cirq.rz(theta[9]).on(qubits[0]))
    circuit.append(cirq.rz(theta[10]).on(qubits[1]))
    circuit.append(cirq.rz(theta[11]).on(qubits[2]))

    return circuit
