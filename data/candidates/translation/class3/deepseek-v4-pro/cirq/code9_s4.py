# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    theta = [sympy.Symbol(f'θ[{i}]') for i in range(6)]

    return cirq.Circuit([
        cirq.Moment(
            cirq.ry(theta[0]).on(qubits[0]),
            cirq.ry(theta[1]).on(qubits[1]),
            cirq.ry(theta[2]).on(qubits[2]),
        ),
        cirq.Moment(cirq.Barrier(3).on(*qubits)),
        cirq.Moment(
            cirq.rz(theta[3]).on(qubits[0]),
            cirq.rz(theta[4]).on(qubits[1]),
            cirq.rz(theta[5]).on(qubits[2]),
        ),
        cirq.Moment(cirq.Barrier(3).on(*qubits)),
        cirq.Moment(cirq.CNOT(qubits[0], qubits[1])),
        cirq.Moment(cirq.CNOT(qubits[0], qubits[2])),
        cirq.Moment(cirq.CNOT(qubits[1], qubits[2])),
        cirq.Moment(cirq.Barrier(3).on(*qubits)),
    ])
