# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    param_idx = 0

    def rotation_layer():
        nonlocal param_idx
        ops = []
        for q in qubits:
            ops.append(cirq.ry(sympy.Symbol(f'theta_{param_idx}'))(q))
            param_idx += 1
        for q in qubits:
            ops.append(cirq.rz(sympy.Symbol(f'theta_{param_idx}'))(q))
            param_idx += 1
        return ops

    for rep in range(reps):
        circuit.append(rotation_layer())
        circuit.append(cirq.Moment([cirq.I(q) for q in qubits]))
        for i in range(num_qubits - 1):
            for j in range(i + 1, num_qubits):
                circuit.append(cirq.CNOT(qubits[i], qubits[j]))
        circuit.append(cirq.Moment([cirq.I(q) for q in qubits]))

    circuit.append(rotation_layer())
    return circuit
