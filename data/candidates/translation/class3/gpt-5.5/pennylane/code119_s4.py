# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    ops = []

    def maj(carry, a, b):
        ops.append(qml.CNOT(wires=[carry, b]))
        ops.append(qml.CNOT(wires=[carry, a]))
        ops.append(qml.Toffoli(wires=[a, b, carry]))

    def uma(carry, a, b):
        ops.append(qml.Toffoli(wires=[a, b, carry]))
        ops.append(qml.CNOT(wires=[carry, a]))
        ops.append(qml.CNOT(wires=[a, b]))

    n = num_state_qubits

    if kind == "full":
        carry = 0
        a_wires = list(range(1, n + 1))
        b_wires = list(range(n + 1, 2 * n + 1))
        cout = 2 * n + 1

        for i in range(n):
            maj(carry, a_wires[i], b_wires[i])

        ops.append(qml.CNOT(wires=[carry, cout]))

        for i in reversed(range(n)):
            uma(carry, a_wires[i], b_wires[i])

    elif kind == "half":
        a_wires = list(range(n))
        b_wires = list(range(n, 2 * n))
        cout = 2 * n
        carry = 2 * n + 1

        for i in range(n):
            maj(carry, a_wires[i], b_wires[i])

        ops.append(qml.CNOT(wires=[carry, cout]))

        for i in reversed(range(n)):
            uma(carry, a_wires[i], b_wires[i])

    else:
        a_wires = list(range(n))
        b_wires = list(range(n, 2 * n))
        carry = 2 * n

        for i in range(n):
            maj(carry, a_wires[i], b_wires[i])

        for i in reversed(range(n)):
            uma(carry, a_wires[i], b_wires[i])

    return qml.tape.QuantumScript(ops, [])
