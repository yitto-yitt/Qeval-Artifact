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

    def su2_layer(prefix):
        nonlocal param_index
        ops = []
        for q in qubits:
            ry = sympy.Symbol(f"{prefix}_ry_{param_index}")
            param_index += 1
            ops.append(cirq.ry(ry).on(q))
        for q in qubits:
            rz = sympy.Symbol(f"{prefix}_rz_{param_index}")
            param_index += 1
            ops.append(cirq.rz(rz).on(q))
        return ops

    circuit.append(su2_layer("l0"))
    if insert_barriers:
        circuit.append(cirq.Moment())

    for r in range(reps):
        for i in range(num_qubits - 1):
            circuit.append(cirq.CNOT(qubits[i], qubits[i + 1]))
        if insert_barriers:
            circuit.append(cirq.Moment())
        circuit.append(su2_layer(f"l{r + 1}"))
        if insert_barriers and r < reps - 1:
            circuit.append(cirq.Moment())

    return circuit
