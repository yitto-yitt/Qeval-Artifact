# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be >= 1")

    if kind == "full":
        total_qubits = 2 * num_state_qubits + 2
    elif kind == "half":
        total_qubits = 2 * num_state_qubits + 1
    else:  # fixed
        total_qubits = 2 * num_state_qubits

    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(total_qubits)

    prog = QProg()

    def majority(a, b, c):
        m = QCircuit()
        m << CNOT(c, b)
        m << CNOT(c, a)
        m << Toffoli(a, b, c)
        return m

    def unmajority(a, b, c):
        u = QCircuit()
        u << Toffoli(a, b, c)
        u << CNOT(c, a)
        u << CNOT(a, b)
        return u

    if kind == "full":
        cin = qubits[0]
        a = [qubits[1 + i] for i in range(num_state_qubits)]
        b = [qubits[1 + num_state_qubits + i] for i in range(num_state_qubits)]
        cout = qubits[-1]

        prog << majority(cin, b[0], a[0])
        for i in range(1, num_state_qubits):
            prog << majority(a[i - 1], b[i], a[i])
        prog << CNOT(a[num_state_qubits - 1], cout)
        for i in range(num_state_qubits - 1, 0, -1):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(cin, b[0], a[0])

    elif kind == "half":
        a = [qubits[i] for i in range(num_state_qubits)]
        b = [qubits[num_state_qubits + i] for i in range(num_state_qubits)]
        cout = qubits[-1]

        prog << majority(a[0], b[0], a[1] if num_state_qubits > 1 else cout)
        if num_state_qubits > 1:
            for i in range(1, num_state_qubits - 1):
                prog << majority(a[i], b[i], a[i + 1])
            prog << majority(a[num_state_qubits - 1], b[num_state_qubits - 1], cout)
            for i in range(num_state_qubits - 1, 0, -1):
                prog << unmajority(a[i - 1], b[i - 1], a[i])
            prog << unmajority(a[0], b[0], a[1])
        else:
            prog << CNOT(a[0], b[0])

    else:  # fixed
        a = [qubits[i] for i in range(num_state_qubits)]
        b = [qubits[num_state_qubits + i] for i in range(num_state_qubits)]

        anc = machine.qAlloc()
        prog << majority(anc, b[0], a[0])
        for i in range(1, num_state_qubits):
            prog << majority(a[i - 1], b[i], a[i])
        for i in range(num_state_qubits - 1, 0, -1):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(anc, b[0], a[0])

    return prog
