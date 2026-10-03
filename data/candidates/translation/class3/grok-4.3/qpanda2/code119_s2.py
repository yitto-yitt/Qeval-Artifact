# EVAL_META: task_id=119, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)
def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == 'full':
        total = 2 * num_state_qubits + 2
        cin = num_state_qubits * 2
        cout = cin + 1
    elif kind == 'half':
        total = 2 * num_state_qubits + 1
        cin = None
        cout = num_state_qubits * 2
    else:
        total = 2 * num_state_qubits + 1
        cin = None
        cout = num_state_qubits * 2
    qs = qubits[:total]
    prog = create_empty_circuit()
    a = qs[:num_state_qubits]
    b = qs[num_state_qubits:2 * num_state_qubits]
    carry = qs[2 * num_state_qubits:]
    if cin is not None:
        prog << CNOT(qs[cin], b[0])
        prog << CNOT(qs[cin], a[0])
        prog << Toffoli(qs[cin], b[0], a[0])
    for i in range(num_state_qubits - 1):
        prog << CNOT(a[i], b[i + 1])
        prog << CNOT(a[i], carry[i])
        prog << Toffoli(b[i + 1], carry[i], a[i])
    if kind != 'half':
        prog << CNOT(a[num_state_qubits - 1], carry[-1])
    for i in range(num_state_qubits - 2, -1, -1):
        prog << Toffoli(b[i + 1], carry[i], a[i])
        prog << CNOT(a[i], carry[i])
        prog << CNOT(a[i], b[i + 1])
    if cin is not None:
        prog << Toffoli(qs[cin], b[0], a[0])
        prog << CNOT(qs[cin], a[0])
        prog << CNOT(qs[cin], b[0])
    return prog
machine.finalize()
