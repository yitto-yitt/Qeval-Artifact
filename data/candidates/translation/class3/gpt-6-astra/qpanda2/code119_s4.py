# EVAL_META: task_id=119, framework=qpanda2, class=3
import atexit
import operator
from pyqpanda import CPUQVM, QCircuit, QProg, CNOT, Toffoli

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
atexit.register(lambda: machine.finalize())


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = operator.index(num_state_qubits)
    if n < 1:
        raise ValueError("num_state_qubits must be at least 1.")
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'.")

    required = 2 * n + (1 if kind == "fixed" else 2)
    if required > len(qubits):
        raise ValueError("The requested adder exceeds the global QVM qubit pool.")

    if kind == "full":
        carry = qubits[0]
        a = qubits[1:n + 1]
        b = qubits[n + 1:2 * n + 1]
        carry_out = qubits[2 * n + 1]
    else:
        a = qubits[:n]
        b = qubits[n:2 * n]
        carry_out = qubits[2 * n] if kind == "half" else None
        carry = qubits[required - 1]

    circuit = QCircuit()

    for i in range(n):
        incoming = carry if i == 0 else a[i - 1]
        circuit << CNOT(a[i], b[i])
        circuit << CNOT(a[i], incoming)
        circuit << Toffoli(incoming, b[i], a[i])

    if carry_out is not None:
        circuit << CNOT(a[-1], carry_out)

    for i in range(n - 1, -1, -1):
        incoming = carry if i == 0 else a[i - 1]
        circuit << Toffoli(incoming, b[i], a[i])
        circuit << CNOT(a[i], incoming)
        circuit << CNOT(incoming, b[i])

    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
