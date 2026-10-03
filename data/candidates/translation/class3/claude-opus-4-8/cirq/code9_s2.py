# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    param_index = 0

    def su2_layer(prefix):
        nonlocal param_index
        for q in qubits:
            theta = sympy.Symbol(f"θ[{param_index}]")
            param_index += 1
            circuit.append(cirq.ry(theta).on(q))
        for q in qubits:
            phi = sympy.Symbol(f"θ[{param_index}]")
            param_index += 1
            circuit.append(cirq.rz(phi).on(q))

    for r in range(reps):
        su2_layer(r)
        circuit.append(cirq.Moment())  # barrier
        for i in range(num_qubits - 1):
            circuit.append(cirq.CNOT(qubits[i], qubits[i + 1]))
        circuit.append(cirq.Moment())  # barrier

    su2_layer(reps)

    return circuit
