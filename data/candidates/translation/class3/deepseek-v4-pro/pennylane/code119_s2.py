# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind == "full":
        num_qubits = 2 * n + 2
    elif kind == "half":
        num_qubits = 2 * n + 1
    else:  # "fixed"
        num_qubits = 2 * n + 2

    ops = []
    if kind in ("full", "fixed"):
        cin = 0
        a = list(range(1, n + 1))
        b = list(range(n + 1, 2 * n + 1))
        cout = 2 * n + 1
    else:  # "half"
        cin = 0
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        cout = 2 * n

    # Forward MAJ gates
    for i in range(n):
        ai = a[i]
        bi = b[i]
        ops.append(qml.Toffoli(wires=[cin, ai, bi]))
        ops.append(qml.CNOT(wires=[cin, ai]))
        ops.append(qml.Toffoli(wires=[ai, bi, cin]))

    # Backward UMA gates
    for i in range(n - 1, -1, -1):
        ai = a[i]
        bi = b[i]
        ops.append(qml.Toffoli(wires=[ai, bi, cin]))
        ops.append(qml.CNOT(wires=[cin, ai]))
        ops.append(qml.Toffoli(wires=[cin, ai, bi]))

    if kind == "full":
        ops.append(qml.CNOT(wires=[cin, cout]))

    return QuantumScript(ops, wires=range(num_qubits))