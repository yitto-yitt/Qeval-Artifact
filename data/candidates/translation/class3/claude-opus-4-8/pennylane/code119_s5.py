# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    ops = []

    def MAJ(a, b, c):
        ops.append(qml.CNOT(wires=[a, b]))
        ops.append(qml.CNOT(wires=[a, c]))
        ops.append(qml.Toffoli(wires=[c, b, a]))

    def UMA(a, b, c):
        ops.append(qml.Toffoli(wires=[c, b, a]))
        ops.append(qml.CNOT(wires=[a, c]))
        ops.append(qml.CNOT(wires=[c, b]))

    if kind == "full":
        cin = 0
        a = [1 + i for i in range(n)]
        b = [1 + n + i for i in range(n)]
        cout = 1 + 2 * n
        has_cout = True
    elif kind == "half":
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cout = 2 * n
        cin = 2 * n + 1  # helper carry-in (|0>)
        has_cout = True
    else:  # fixed
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cin = 2 * n  # helper carry-in (|0>)
        cout = None
        has_cout = False

    # MAJ chain
    MAJ(a[0], b[0], cin)
    for i in range(1, n):
        MAJ(a[i], b[i], a[i - 1])

    if has_cout:
        ops.append(qml.CNOT(wires=[a[n - 1], cout]))

    # UMA chain
    for i in range(n - 1, 0, -1):
        UMA(a[i], b[i], a[i - 1])
    UMA(a[0], b[0], cin)

    return qml.tape.QuantumScript(ops, [], name="CDKMRippleCarryAdder")
