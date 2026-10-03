# EVAL_META: task_id=119, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(128)
atexit.register(machine.finalize)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = int(num_state_qubits)
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    total_qubits = 2 * n + (2 if kind in ("full", "half") else 1)
    if total_qubits > len(_qubits):
        raise ValueError("num_state_qubits is too large for the allocated global QVM qubit pool")

    q = _qubits[:total_qubits]
    prog = pq.QProg()

    def maj(a, b, c):
        prog << pq.CNOT(a, b)
        prog << pq.CNOT(a, c)
        prog << pq.Toffoli(c, b, a)

    def uma(a, b, c):
        prog << pq.Toffoli(c, b, a)
        prog << pq.CNOT(a, c)
        prog << pq.CNOT(c, b)

    if kind == "full":
        cin = q[0]
        a_reg = [q[1 + i] for i in range(n)]
        b_reg = [q[1 + n + i] for i in range(n)]
        cout = q[1 + 2 * n]
        carry_in = cin
    elif kind == "half":
        a_reg = [q[i] for i in range(n)]
        b_reg = [q[n + i] for i in range(n)]
        cout = q[2 * n]
        carry_in = q[2 * n + 1]
    else:
        a_reg = [q[i] for i in range(n)]
        b_reg = [q[n + i] for i in range(n)]
        cout = None
        carry_in = q[2 * n]

    maj(a_reg[0], b_reg[0], carry_in)

    for i in range(1, n):
        maj(a_reg[i], b_reg[i], a_reg[i - 1])

    if cout is not None:
        prog << pq.CNOT(a_reg[n - 1], cout)

    for i in range(n - 1, 0, -1):
        uma(a_reg[i], b_reg[i], a_reg[i - 1])

    uma(a_reg[0], b_reg[0], carry_in)

    return prog
