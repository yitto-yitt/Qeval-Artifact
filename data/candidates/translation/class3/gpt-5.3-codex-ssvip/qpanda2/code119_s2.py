# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(512)


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be one of: 'full', 'half', 'fixed'")
    if num_state_qubits <= 0:
        raise ValueError("num_state_qubits must be positive")

    n = num_state_qubits
    if kind == "full":
        total = 2 * n + 2
        cin = _global_qubits[0]
        a = _global_qubits[1:1 + n]
        b = _global_qubits[1 + n:1 + 2 * n]
        cout = _global_qubits[1 + 2 * n]
    elif kind == "half":
        total = 2 * n + 2
        cin = None
        a = _global_qubits[0:n]
        b = _global_qubits[n:2 * n]
        cout = _global_qubits[2 * n]
    else:  # fixed
        total = 2 * n + 1
        cin = None
        a = _global_qubits[0:n]
        b = _global_qubits[n:2 * n]
        cout = None

    prog = pq.QProg()

    def majority(c, x, y):
        seq = pq.QCircuit()
        seq << pq.CNOT(y, x) << pq.CNOT(y, c) << pq.Toffoli(c, x, y)
        return seq

    def unmajority(c, x, y):
        seq = pq.QCircuit()
        seq << pq.Toffoli(c, x, y) << pq.CNOT(y, c) << pq.CNOT(c, x)
        return seq

    if kind == "full":
        prog << majority(cin, b[0], a[0])
        for i in range(1, n):
            prog << majority(a[i - 1], b[i], a[i])
        prog << pq.CNOT(a[n - 1], cout)
        for i in reversed(range(1, n)):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(cin, b[0], a[0])

    elif kind == "half":
        anc = cout
        prog << majority(anc, b[0], a[0])
        for i in range(1, n):
            prog << majority(a[i - 1], b[i], a[i])
        prog << pq.CNOT(a[n - 1], anc)
        for i in reversed(range(1, n)):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(anc, b[0], a[0])

    else:  # fixed
        anc = _global_qubits[2 * n]
        prog << majority(anc, b[0], a[0])
        for i in range(1, n):
            prog << majority(a[i - 1], b[i], a[i])
        for i in reversed(range(1, n)):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(anc, b[0], a[0])

    return prog


machine.finalize()
