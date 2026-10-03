# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(512)


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits <= 0:
        raise ValueError("num_state_qubits must be positive")

    n = num_state_qubits
    if kind == "full":
        total = 2 * n + 2
        cin = 0
        a_start = 1
        b_start = 1 + n
        cout = 2 * n + 1
    elif kind == "half":
        total = 2 * n + 2
        cin = None
        a_start = 0
        b_start = n
        cout = 2 * n + 1
    else:  # fixed
        total = 2 * n + 1
        cin = None
        a_start = 0
        b_start = n
        cout = None

    q = _global_qubits[:total]
    prog = pq.QProg()

    def MAJ(c, b, a):
        return pq.QCircuit() << pq.CNOT(a, b) << pq.CNOT(a, c) << pq.Toffoli(c, b, a)

    def UMA(c, b, a):
        return pq.QCircuit() << pq.Toffoli(c, b, a) << pq.CNOT(a, c) << pq.CNOT(c, b)

    if kind == "full":
        prog << MAJ(q[cin], q[b_start + 0], q[a_start + 0])
        for i in range(1, n):
            prog << MAJ(q[a_start + i - 1], q[b_start + i], q[a_start + i])
        prog << pq.CNOT(q[a_start + n - 1], q[cout])
        for i in reversed(range(1, n)):
            prog << UMA(q[a_start + i - 1], q[b_start + i], q[a_start + i])
        prog << UMA(q[cin], q[b_start + 0], q[a_start + 0])

    elif kind == "half":
        anc = q[cout]
        prog << MAJ(anc, q[b_start + 0], q[a_start + 0])
        for i in range(1, n):
            prog << MAJ(q[a_start + i - 1], q[b_start + i], q[a_start + i])
        prog << pq.CNOT(q[a_start + n - 1], anc)
        for i in reversed(range(1, n)):
            prog << UMA(q[a_start + i - 1], q[b_start + i], q[a_start + i])
        prog << UMA(anc, q[b_start + 0], q[a_start + 0])

    else:  # fixed
        anc = q[2 * n]
        prog << MAJ(anc, q[b_start + 0], q[a_start + 0])
        for i in range(1, n):
            prog << MAJ(q[a_start + i - 1], q[b_start + i], q[a_start + i])
        for i in reversed(range(1, n)):
            prog << UMA(q[a_start + i - 1], q[b_start + i], q[a_start + i])
        prog << UMA(anc, q[b_start + 0], q[a_start + 0])

    machine.finalize()
    return prog
