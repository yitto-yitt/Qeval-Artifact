# EVAL_META: task_id=119, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2048)
atexit.register(machine.finalize)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be at least 1")
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    n = num_state_qubits
    required = 2 * n + (2 if kind in ("full", "half") else 1)
    if required > len(qubits):
        raise ValueError("not enough globally allocated qubits")

    circuit = QCircuit()

    def maj(a, b, c):
        circuit.insert(CNOT(a, b))
        circuit.insert(CNOT(a, c))
        circuit.insert(Toffoli(c, b, a))

    def uma(a, b, c):
        circuit.insert(Toffoli(c, b, a))
        circuit.insert(CNOT(a, c))
        circuit.insert(CNOT(c, b))

    if kind == "full":
        cin = qubits[0]
        a_reg = [qubits[i] for i in range(1, n + 1)]
        b_reg = [qubits[i] for i in range(n + 1, 2 * n + 1)]
        cout = qubits[2 * n + 1]
    elif kind == "half":
        a_reg = [qubits[i] for i in range(n)]
        b_reg = [qubits[i] for i in range(n, 2 * n)]
        cout = qubits[2 * n]
        cin = qubits[2 * n + 1]
    else:
        a_reg = [qubits[i] for i in range(n)]
        b_reg = [qubits[i] for i in range(n, 2 * n)]
        cin = qubits[2 * n]
        cout = None

    maj(a_reg[0], b_reg[0], cin)

    for i in range(1, n):
        maj(a_reg[i], b_reg[i], a_reg[i - 1])

    if cout is not None:
        circuit.insert(CNOT(a_reg[n - 1], cout))

    for i in range(n - 1, 0, -1):
        uma(a_reg[i], b_reg[i], a_reg[i - 1])

    uma(a_reg[0], b_reg[0], cin)

    return circuit
