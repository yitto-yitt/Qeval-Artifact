# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    insert_barriers = True

    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()

    param_index = 0

    def rotation_layer(prefix):
        nonlocal param_index
        for q in qubits:
            ry = sympy.Symbol(f"{prefix}_ry_{q}_{param_index}")
            rz = sympy.Symbol(f"{prefix}_rz_{q}_{param_index}")
            circuit.append(cirq.ry(ry).on(q))
            circuit.append(cirq.rz(rz).on(q))
            param_index += 1

    def entanglement_layer():
        for i in range(num_qubits - 1):
            for j in range(i + 1, num_qubits):
                circuit.append(cirq.CNOT(qubits[i], qubits[j]))

    for rep in range(reps):
        rotation_layer(f"rep{rep}")
        if insert_barriers:
            circuit.append(cirq.Moment())
        entanglement_layer()
        if insert_barriers:
            circuit.append(cirq.Moment())

    rotation_layer("final")

    return circuit
