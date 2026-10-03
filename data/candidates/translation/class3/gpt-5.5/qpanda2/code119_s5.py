# EVAL_META: task_id=119, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(30)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be at least 1")

    n = num_state_qubits
    needed = 2 * n + (2 if kind in ("full", "half") else 1)
    if needed > len(qubits):
        raise ValueError("not enough globally allocated qubits")

    circuit = QCircuit()

    if kind == "full":
        cin = qubits[0]
        a = qubits[1:1 + n]
        b = qubits[1 + n:1 + 2 * n]
        cout = qubits[1 + 2 * n]
        carry_in = cin
    elif kind == "half":
        a = qubits[0:n]
        b = qubits[n:2 * n]
        cout = qubits[2 * n]
        carry_in = qubits[2 * n + 1]
    else:
        a = qubits[0:n]
        b = qubits[n:2 * n]
        carry_in = qubits[2 * n]
        cout = None

    def maj(carry, bq, aq):
        circuit.insert(CNOT(aq, bq))
        circuit.insert(CNOT(aq, carry))
        circuit.insert(Toffoli(carry, bq, aq))

    def uma(carry, bq, aq):
        circuit.insert(Toffoli(carry, bq, aq))
        circuit.insert(CNOT(aq, carry))
        circuit.insert(CNOT(carry, bq))

    maj(carry_in, b[0], a[0])

    for i in range(1, n):
        maj(a[i - 1], b[i], a[i])

    if kind in ("full", "half"):
        circuit.insert(CNOT(a[n - 1], cout))

    for i in range(n - 1, 0, -1):
        uma(a[i - 1], b[i], a[i])

    uma(carry_in, b[0], a[0])

    return circuit

atexit.register(machine.finalize)
