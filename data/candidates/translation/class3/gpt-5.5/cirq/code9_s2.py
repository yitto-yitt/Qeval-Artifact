# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    params = [sympy.Symbol(f"θ[{i}]") for i in range(12)]

    def barrier_op():
        if hasattr(cirq, "barrier"):
            return cirq.barrier(*qubits)
        if hasattr(cirq, "BarrierGate"):
            return cirq.BarrierGate(3).on(*qubits)
        return cirq.IdentityGate(3).on(*qubits)

    circuit = cirq.Circuit([
        cirq.Moment([cirq.ry(params[i]).on(qubits[i]) for i in range(3)]),
        cirq.Moment([cirq.rz(params[i + 3]).on(qubits[i]) for i in range(3)]),
        cirq.Moment([barrier_op()]),
        cirq.Moment([cirq.CNOT(qubits[2], qubits[1])]),
        cirq.Moment([cirq.CNOT(qubits[1], qubits[0])]),
        cirq.Moment([barrier_op()]),
        cirq.Moment([cirq.ry(params[i + 6]).on(qubits[i]) for i in range(3)]),
        cirq.Moment([cirq.rz(params[i + 9]).on(qubits[i]) for i in range(3)]),
    ])
    return circuit
