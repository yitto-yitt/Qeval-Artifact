# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be >= 1")

    machine = CPUQVM()
    machine.init_qvm()

    if kind == "full":
        total_qubits = 2 * num_state_qubits + 2
    elif kind == "half":
        total_qubits = 2 * num_state_qubits + 1
    else:  # fixed
        total_qubits = 2 * num_state_qubits

    q = machine.qAlloc_many(total_qubits)
    prog = QProg()

    def majority(a, b, c):
        return QCircuit() << CNOT(c, b) << CNOT(c, a) << Toffoli(a, b, c)

    def unmajority(a, b, c):
        return QCircuit() << Toffoli(a, b, c) << CNOT(c, a) << CNOT(a, b)

    if kind == "full":
        cin = q[0]
        a = [q[i] for i in range(1, 1 + num_state_qubits)]
        b = [q[i] for i in range(1 + num_state_qubits, 1 + 2 * num_state_qubits)]
        cout = q[-1]

        prog << majority(cin, b[0], a[0])
        for i in range(1, num_state_qubits):
            prog << majority(a[i - 1], b[i], a[i])
        prog << CNOT(a[num_state_qubits - 1], cout)
        for i in reversed(range(1, num_state_qubits)):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(cin, b[0], a[0])

    elif kind == "half":
        a = [q[i] for i in range(0, num_state_qubits)]
        b = [q[i] for i in range(num_state_qubits, 2 * num_state_qubits)]
        cout = q[-1]

        prog << majority(a[0], b[0], a[1] if num_state_qubits > 1 else cout)
        if num_state_qubits > 1:
            for i in range(1, num_state_qubits - 1):
                prog << majority(a[i], b[i], a[i + 1])
            prog << CNOT(a[num_state_qubits - 1], cout)
            for i in reversed(range(1, num_state_qubits - 1)):
                prog << unmajority(a[i], b[i], a[i + 1])
            prog << unmajority(a[0], b[0], a[1])

    else:  # fixed
        a = [q[i] for i in range(0, num_state_qubits)]
        b = [q[i] for i in range(num_state_qubits, 2 * num_state_qubits)]

        anc = machine.qAlloc()
        prog << majority(anc, b[0], a[0])
        for i in range(1, num_state_qubits):
            prog << majority(a[i - 1], b[i], a[i])
        for i in reversed(range(1, num_state_qubits)):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(anc, b[0], a[0])

    return prog
