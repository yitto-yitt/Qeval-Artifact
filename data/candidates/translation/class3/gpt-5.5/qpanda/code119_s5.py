# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be at least 1")

    n = num_state_qubits

    if kind == "full":
        total_qubits = 2 * n + 2
        carry = 0
        a = [1 + i for i in range(n)]
        b = [1 + n + i for i in range(n)]
        cout = 2 * n + 1
    elif kind == "half":
        total_qubits = 2 * n + 2
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cout = 2 * n
        carry = 2 * n + 1
    else:
        total_qubits = 2 * n + 1
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cout = None
        carry = 2 * n

    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        q = machine.qAlloc_many(total_qubits)
    elif hasattr(machine, "qAllocMany"):
        q = machine.qAllocMany(total_qubits)
    else:
        q = [machine.qAlloc() for _ in range(total_qubits)]

    prog = QProg()

    def append_gate(gate):
        nonlocal prog
        prog << gate

    def ccx(c1, c2, t):
        try:
            return Toffoli(q[c1], q[c2], q[t])
        except NameError:
            return X(q[t]).control([q[c1], q[c2]])

    def maj(c, ai, bi):
        append_gate(CNOT(q[ai], q[bi]))
        append_gate(CNOT(q[ai], q[c]))
        append_gate(ccx(c, bi, ai))

    def uma(c, ai, bi):
        append_gate(ccx(c, bi, ai))
        append_gate(CNOT(q[ai], q[c]))
        append_gate(CNOT(q[c], q[bi]))

    maj(carry, a[0], b[0])
    for i in range(1, n):
        maj(a[i - 1], a[i], b[i])

    if cout is not None:
        append_gate(CNOT(q[a[n - 1]], q[cout]))

    for i in range(n - 1, 0, -1):
        uma(a[i - 1], a[i], b[i])
    uma(carry, a[0], b[0])

    if not hasattr(create_ripple_carry_adder_circuit, "_machines"):
        create_ripple_carry_adder_circuit._machines = []
    create_ripple_carry_adder_circuit._machines.append(machine)

    return prog
