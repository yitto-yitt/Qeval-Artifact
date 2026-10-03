# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(512)


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    n = int(num_state_qubits)
    if n <= 0:
        raise ValueError("num_state_qubits must be positive")

    if kind == "full":
        total = 2 * n + 2
        cin_idx = 0
        a_start = 1
        b_start = 1 + n
        cout_idx = total - 1
    elif kind == "half":
        total = 2 * n + 1
        cin_idx = None
        a_start = 0
        b_start = n
        cout_idx = total - 1
    else:  # fixed
        total = 2 * n
        cin_idx = None
        a_start = 0
        b_start = n
        cout_idx = None

    q = _global_qubits[:total]
    a = q[a_start:a_start + n]
    b = q[b_start:b_start + n]
    cin_q = q[cin_idx] if cin_idx is not None else None
    cout_q = q[cout_idx] if cout_idx is not None else None

    prog = pq.QProg()

    def majority(x, y, z):
        c = pq.QCircuit()
        c.insert(pq.CNOT(z, y))
        c.insert(pq.CNOT(z, x))
        c.insert(pq.Toffoli(x, y, z))
        return c

    def unmajority(x, y, z):
        c = pq.QCircuit()
        c.insert(pq.Toffoli(x, y, z))
        c.insert(pq.CNOT(z, x))
        c.insert(pq.CNOT(x, y))
        return c

    if kind == "full":
        prog.insert(majority(cin_q, b[0], a[0]))
        for i in range(1, n):
            prog.insert(majority(a[i - 1], b[i], a[i]))
        prog.insert(pq.CNOT(a[n - 1], cout_q))
        for i in reversed(range(1, n)):
            prog.insert(unmajority(a[i - 1], b[i], a[i]))
        prog.insert(unmajority(cin_q, b[0], a[0]))
    elif kind == "half":
        anc = cout_q
        prog.insert(majority(anc, b[0], a[0]))
        for i in range(1, n):
            prog.insert(majority(a[i - 1], b[i], a[i]))
        prog.insert(pq.CNOT(a[n - 1], anc))
        for i in reversed(range(1, n)):
            prog.insert(unmajority(a[i - 1], b[i], a[i]))
        prog.insert(unmajority(anc, b[0], a[0]))
    else:  # fixed
        anc = a[n - 1]
        prog.insert(majority(anc, b[0], a[0]))
        for i in range(1, n - 1):
            prog.insert(majority(a[i - 1], b[i], a[i]))
        if n > 1:
            prog.insert(pq.CNOT(a[n - 2], b[n - 1]))
            for i in reversed(range(1, n - 1)):
                prog.insert(unmajority(a[i - 1], b[i], a[i]))
        prog.insert(unmajority(anc, b[0], a[0]))

    machine.directly_run(prog)
    machine.finalize()
    return prog
