# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be one of: 'full', 'half', 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be >= 1")

    qvm = CPUQVM()
    qvm.init_qvm()

    n = num_state_qubits
    if kind == "full":
        total_qubits = 2 * n + 2
    elif kind == "half":
        total_qubits = 2 * n + 1
    else:  # fixed
        total_qubits = 2 * n + 1

    qubits = qvm.qAlloc_many(total_qubits)
    prog = QProg()
    circuit = QCircuit()

    if kind == "full":
        cin = qubits[0]
        a = [qubits[1 + i] for i in range(n)]
        b = [qubits[1 + n + i] for i in range(n)]
        cout = qubits[-1]

        for i in range(n):
            circuit << CNOT(a[i], b[i])
        circuit << CNOT(cin, b[0])

        for i in range(n - 1):
            circuit << X(b[i + 1]).control([a[i], b[i]])
            circuit << CNOT(a[i], b[i + 1])
            circuit << X(b[i + 1]).control([cin if i == 0 else b[i], a[i]])
        circuit << X(cout).control([a[n - 1], b[n - 1]])
        circuit << CNOT(a[n - 1], cout)
        circuit << X(cout).control([cin if n == 1 else b[n - 1], a[n - 1]])

        for i in reversed(range(n - 1)):
            circuit << X(b[i + 1]).control([cin if i == 0 else b[i], a[i]])
            circuit << CNOT(a[i], b[i + 1])
            circuit << X(b[i + 1]).control([a[i], b[i]])

        circuit << CNOT(cin, b[0])
        for i in range(n):
            circuit << CNOT(a[i], b[i])

    elif kind == "half":
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        cout = qubits[-1]

        for i in range(n):
            circuit << CNOT(a[i], b[i])

        for i in range(n - 1):
            circuit << X(b[i + 1]).control([a[i], b[i]])
            circuit << CNOT(a[i], b[i + 1])
            circuit << X(b[i + 1]).control([b[i], a[i]])
        circuit << X(cout).control([a[n - 1], b[n - 1]])
        circuit << CNOT(a[n - 1], cout)
        circuit << X(cout).control([b[n - 1], a[n - 1]])

        for i in reversed(range(n - 1)):
            circuit << X(b[i + 1]).control([b[i], a[i]])
            circuit << CNOT(a[i], b[i + 1])
            circuit << X(b[i + 1]).control([a[i], b[i]])

        for i in range(n):
            circuit << CNOT(a[i], b[i])

    else:  # fixed
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        anc = qubits[-1]

        for i in range(n):
            circuit << CNOT(a[i], b[i])

        circuit << X(anc).control([a[0], b[0]])
        for i in range(1, n):
            circuit << X(b[i]).control([a[i - 1], b[i - 1]])
            circuit << CNOT(a[i - 1], b[i])
            circuit << X(b[i]).control([b[i - 1], a[i - 1]])

        for i in reversed(range(1, n)):
            circuit << X(b[i]).control([b[i - 1], a[i - 1]])
            circuit << CNOT(a[i - 1], b[i])
            circuit << X(b[i]).control([a[i - 1], b[i - 1]])
        circuit << X(anc).control([a[0], b[0]])

        for i in range(n):
            circuit << CNOT(a[i], b[i])

    prog << circuit
    return prog
