# EVAL_META: task_id=119, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2048)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be at least 1")

    if kind == "full":
        total_qubits = 2 * num_state_qubits + 2
        cin = q[0]
        a = [q[i] for i in range(1, num_state_qubits + 1)]
        b = [q[i] for i in range(num_state_qubits + 1, 2 * num_state_qubits + 1)]
        cout = q[2 * num_state_qubits + 1]
    elif kind == "half":
        total_qubits = 2 * num_state_qubits + 2
        a = [q[i] for i in range(num_state_qubits)]
        b = [q[i] for i in range(num_state_qubits, 2 * num_state_qubits)]
        cout = q[2 * num_state_qubits]
        cin = q[2 * num_state_qubits + 1]
    else:
        total_qubits = 2 * num_state_qubits + 1
        a = [q[i] for i in range(num_state_qubits)]
        b = [q[i] for i in range(num_state_qubits, 2 * num_state_qubits)]
        cin = q[2 * num_state_qubits]
        cout = None

    if total_qubits > len(q):
        raise ValueError("not enough globally allocated qubits")

    circuit = QCircuit()

    def maj(x, y, z):
        circuit.insert(CNOT(x, y))
        circuit.insert(CNOT(x, z))
        circuit.insert(Toffoli(z, y, x))

    def uma(x, y, z):
        circuit.insert(Toffoli(z, y, x))
        circuit.insert(CNOT(x, z))
        circuit.insert(CNOT(z, y))

    maj(a[0], b[0], cin)

    for i in range(num_state_qubits - 1):
        maj(a[i + 1], b[i + 1], a[i])

    if kind in ("full", "half"):
        circuit.insert(CNOT(a[num_state_qubits - 1], cout))

    for i in reversed(range(num_state_qubits - 1)):
        uma(a[i + 1], b[i + 1], a[i])

    uma(a[0], b[0], cin)

    return circuit

atexit.register(lambda: machine.finalize())
