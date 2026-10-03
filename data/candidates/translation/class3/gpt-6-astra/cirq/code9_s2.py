# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy


def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    parameters = [sympy.Symbol(f"θ[{i}]") for i in range(12)]
    moments = []

    for layer in range(2):
        offset = 6 * layer
        moments.append(
            cirq.Moment(
                cirq.ry(parameters[offset + i])(qubits[i])
                for i in range(3)
            )
        )
        moments.append(
            cirq.Moment(
                cirq.rz(parameters[offset + 3 + i])(qubits[i])
                for i in range(3)
            )
        )
        if layer == 0:
            moments.append(cirq.Moment([cirq.CNOT(qubits[1], qubits[2])]))
            moments.append(cirq.Moment([cirq.CNOT(qubits[0], qubits[1])]))

    return cirq.Circuit(moments)
