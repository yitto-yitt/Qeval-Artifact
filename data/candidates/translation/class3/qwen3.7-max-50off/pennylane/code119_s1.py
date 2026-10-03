# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    ops = []
    
    a = list(range(n))
    b = list(range(n, 2 * n))
    
    if kind == 'full':
        cin = 2 * n
        cout = 2 * n + 1
    elif kind == 'half':
        cin = None
        cout = 2 * n
    elif kind == 'fixed':
        cin = None
        cout = None
    else:
        raise ValueError("Invalid kind")

    def maj(x, y, z):
        ops.append(qml.CNOT(wires=[z, y]))
        ops.append(qml.CNOT(wires=[z, x]))
        ops.append(qml.Toffoli(wires=[x, y, z]))

    def uma(x, y, z):
        ops.append(qml.Toffoli(wires=[x, y, z]))
        ops.append(qml.CNOT(wires=[z, x]))
        ops.append(qml.CNOT(wires=[x, y]))

    if kind == 'full':
        maj(cin, b[0], a[0])
    else:
        ops.append(qml.CNOT(wires=[a[0], b[0]]))

    for i in range(1, n):
        maj(a[i - 1], b[i], a[i])

    if kind != 'fixed':
        ops.append(qml.CNOT(wires=[a[-1], cout]))

    for i in range(n - 1, 0, -1):
        uma(a[i - 1], b[i], a[i])

    if kind == 'full':
        uma(cin, b[0], a[0])

    return qml.tape.QuantumScript(ops, measurements=[])
