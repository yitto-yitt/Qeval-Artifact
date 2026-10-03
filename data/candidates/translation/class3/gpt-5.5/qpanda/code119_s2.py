# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be at least 1")

    n = int(num_state_qubits)

    if kind == "full":
        num_qubits = 2 * n + 2
    elif kind == "half":
        num_qubits = 2 * n + 2
    else:
        num_qubits = 2 * n + 1

    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(num_qubits)
    elif hasattr(qvm, "qalloc_many"):
        qubits = qvm.qalloc_many(num_qubits)
    else:
        qubits = list(range(num_qubits))

    if not hasattr(create_ripple_carry_adder_circuit, "_qvms"):
        create_ripple_carry_adder_circuit._qvms = []
    create_ripple_carry_adder_circuit._qvms.append(qvm)

    circuit = QCircuit()

    def append_gate(gate):
        try:
            circuit.insert(gate)
        except Exception:
            circuit << gate

    def cx(control, target):
        if "CNOT" in globals():
            return CNOT(control, target)
        return CX(control, target)

    def ccx(control1, control2, target):
        if "Toffoli" in globals():
            return Toffoli(control1, control2, target)
        return X(target).control([control1, control2])

    def maj(a, b, c):
        append_gate(cx(a, b))
        append_gate(cx(a, c))
        append_gate(ccx(c, b, a))

    def uma(a, b, c):
        append_gate(ccx(c, b, a))
        append_gate(cx(a, c))
        append_gate(cx(c, b))

    if kind == "full":
        cin = qubits[0]
        a = [qubits[1 + i] for i in range(n)]
        b = [qubits[1 + n + i] for i in range(n)]
        cout = qubits[1 + 2 * n]
        carry_in = cin
    elif kind == "half":
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        cout = qubits[2 * n]
        carry_in = qubits[2 * n + 1]
    else:
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        carry_in = qubits[2 * n]

    maj(a[0], b[0], carry_in)

    for i in range(n - 1):
        maj(a[i + 1], b[i + 1], a[i])

    if kind in ("full", "half"):
        append_gate(cx(a[n - 1], cout))

    for i in reversed(range(n - 1)):
        uma(a[i + 1], b[i + 1], a[i])

    uma(a[0], b[0], carry_in)

    return circuit
