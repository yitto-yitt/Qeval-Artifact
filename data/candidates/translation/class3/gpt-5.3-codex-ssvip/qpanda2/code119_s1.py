# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be >= 1")

    n = num_state_qubits
    total_qubits = 2 * n + (2 if kind == "full" else 1)
    q = machine.qAlloc_many(total_qubits)

    if kind == "full":
        cin = q[0]
        a = q[1:1 + n]
        b = q[1 + n:1 + 2 * n]
        cout = q[-1]
    elif kind == "half":
        a = q[0:n]
        b = q[n:2 * n]
        cout = q[-1]
        cin = None
    else:  # fixed
        a = q[0:n]
        b = q[n:2 * n]
        cin = None
        cout = None

    prog = pq.QProg()

    def majority(c, x, y):
        return pq.CNOT(y, x) << pq.CNOT(y, c) << pq.Toffoli(c, x, y)

    def unmajority(c, x, y):
        return pq.Toffoli(c, x, y) << pq.CNOT(y, c) << pq.CNOT(c, x)

    if n == 1:
        if kind == "full":
            prog << pq.CNOT(a[0], b[0]) << pq.CNOT(cin, b[0]) << pq.Toffoli(cin, a[0], cout)
        elif kind == "half":
            prog << pq.CNOT(a[0], b[0]) << pq.Toffoli(a[0], b[0], cout)
        else:
            prog << pq.CNOT(a[0], b[0])
    else:
        carry_chain = [cin] + a if kind == "full" else a

        prog << majority(carry_chain[0], b[0], carry_chain[1])
        for i in range(1, n - 1):
            prog << majority(carry_chain[i], b[i], carry_chain[i + 1])

        if kind in ("full", "half"):
            prog << pq.CNOT(carry_chain[n - 1], b[n - 1]) << pq.CNOT(b[n - 1], cout)
        else:
            prog << pq.CNOT(carry_chain[n - 1], b[n - 1])

        for i in range(n - 2, 0, -1):
            prog << unmajority(carry_chain[i], b[i], carry_chain[i + 1])
        prog << unmajority(carry_chain[0], b[0], carry_chain[1])

    machine.finalize()
    return prog
