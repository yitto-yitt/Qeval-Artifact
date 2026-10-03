# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be at least 1")

    if not hasattr(create_ripple_carry_adder_circuit, "_machine"):
        machine = CPUQVM()
        if hasattr(machine, "init_qvm"):
            machine.init_qvm()
        elif hasattr(machine, "init"):
            machine.init()
        create_ripple_carry_adder_circuit._machine = machine

    machine = create_ripple_carry_adder_circuit._machine

    total_qubits = 2 * num_state_qubits + (2 if kind in ("full", "half") else 1)

    if hasattr(machine, "qAlloc_many"):
        qubits = list(machine.qAlloc_many(total_qubits))
    elif hasattr(machine, "qalloc_many"):
        qubits = list(machine.qalloc_many(total_qubits))
    else:
        qubits = [machine.qAlloc() for _ in range(total_qubits)]

    if kind == "full":
        cin = qubits[0]
        a = qubits[1:1 + num_state_qubits]
        b = qubits[1 + num_state_qubits:1 + 2 * num_state_qubits]
        cout = qubits[1 + 2 * num_state_qubits]
        carry_in = cin
    elif kind == "half":
        a = qubits[:num_state_qubits]
        b = qubits[num_state_qubits:2 * num_state_qubits]
        cout = qubits[2 * num_state_qubits]
        carry_in = qubits[2 * num_state_qubits + 1]
    else:
        a = qubits[:num_state_qubits]
        b = qubits[num_state_qubits:2 * num_state_qubits]
        cout = None
        carry_in = qubits[2 * num_state_qubits]

    prog = QProg()

    def _ccx(c1, c2, target):
        func = globals().get("Toffoli", None)
        if func is not None:
            return func(c1, c2, target)
        func = globals().get("TOFFOLI", None)
        if func is not None:
            return func(c1, c2, target)
        func = globals().get("CCNOT", None)
        if func is not None:
            return func(c1, c2, target)
        return X(target).control([c1, c2])

    def _maj(carry, bq, aq):
        nonlocal prog
        prog << CNOT(aq, bq)
        prog << CNOT(aq, carry)
        prog << _ccx(carry, bq, aq)

    def _uma(carry, bq, aq):
        nonlocal prog
        prog << _ccx(carry, bq, aq)
        prog << CNOT(aq, carry)
        prog << CNOT(carry, bq)

    _maj(carry_in, b[0], a[0])
    for i in range(1, num_state_qubits):
        _maj(a[i - 1], b[i], a[i])

    if kind in ("full", "half"):
        prog << CNOT(a[-1], cout)

    for i in range(num_state_qubits - 1, 0, -1):
        _uma(a[i - 1], b[i], a[i])
    _uma(carry_in, b[0], a[0])

    return prog
