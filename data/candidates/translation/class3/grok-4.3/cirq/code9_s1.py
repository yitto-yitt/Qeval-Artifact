# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    params = sympy.symbols("theta0:12")
    circuit = cirq.Circuit()
    for i in range(3):
        circuit += cirq.ry(params[2 * i]).on(qubits[i])
        circuit += cirq.rz(params[2 * i + 1]).on(qubits[i])
    circuit += cirq.CNOT(qubits[0], qubits[1])
    circuit += cirq.CNOT(qubits[1], qubits[2])
    for i in range(3):
        circuit += cirq.ry(params[6 + 2 * i]).on(qubits[i])
        circuit += cirq.rz(params[6 + 2 * i + 1]).on(qubits[i])
    return circuit
