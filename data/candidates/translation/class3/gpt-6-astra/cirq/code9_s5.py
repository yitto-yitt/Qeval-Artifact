# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy


def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    parameters = [sympy.Symbol(f"θ[{i}]") for i in range(12)]

    return cirq.Circuit(
        cirq.Moment(cirq.ry(parameters[i])(qubits[i]) for i in range(3)),
        cirq.Moment(cirq.rz(parameters[3 + i])(qubits[i]) for i in range(3)),
        cirq.Moment([cirq.CNOT(qubits[1], qubits[2])]),
        cirq.Moment([cirq.CNOT(qubits[0], qubits[1])]),
        cirq.Moment(cirq.ry(parameters[6 + i])(qubits[i]) for i in range(3)),
        cirq.Moment(cirq.rz(parameters[9 + i])(qubits[i]) for i in range(3)),
    )
