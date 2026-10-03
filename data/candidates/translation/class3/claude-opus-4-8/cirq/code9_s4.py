# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()

    param_index = 0

    def add_rotation_layer():
        nonlocal param_index
        for q in qubits:
            theta = sympy.Symbol(f"θ[{param_index}]")
            param_index += 1
            circuit.append(cirq.ry(theta).on(q))
        for q in qubits:
            phi = sympy.Symbol(f"θ[{param_index}]")
            param_index += 1
            circuit.append(cirq.rz(phi).on(q))

    def add_entanglement_layer():
        for i in range(num_qubits):
            for j in range(i + 1, num_qubits):
                circuit.append(cirq.CNOT(qubits[i], qubits[j]))

    for _ in range(reps):
        add_rotation_layer()
        circuit.append(cirq.Moment())
        add_entanglement_layer()
        circuit.append(cirq.Moment())

    add_rotation_layer()

    return circuit
