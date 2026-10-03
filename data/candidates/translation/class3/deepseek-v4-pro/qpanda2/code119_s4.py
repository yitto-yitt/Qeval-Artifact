# EVAL_META: task_id=119, framework=qpanda2, class=3
import atexit
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.set_configure(64, 64)
machine.init_qvm()
qubits = machine.qAlloc_many(64)


def _allocate_registers(num_state_qubits, kind):
    n = operator.index(num_state_qubits)
    if n < 1:
        raise ValueError("num_state_qubits must be at least 1")
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    if kind == "full":
        total = 2 * n + 2
        carry_in = qubits[0]
        a = qubits[1:n + 1]
        b = qubits[n + 1:2 * n + 1]
        carry_out = qubits[2 * n + 1]
    elif kind == "half":
        total = 2 * n + 2
        a = qubits[:n]
        b = qubits[n:2 * n]
        carry_out = qubits[2 * n]
        carry_in = qubits[2 * n + 1]
    else:
        total = 2 * n + 1
        a = qubits[:n]
        b = qubits[n:2 * n]
        carry_in = qubits[2 * n]
        carry_out = None

    if total > len(qubits):
        raise ValueError("requested circuit exceeds the global qubit pool")
    return n, a, b, carry_in, carry_out


def _forward_pass(circuit, a, b, initial_carry):
    for index, (a_bit, b_bit) in enumerate(zip(a, b)):
        carry = initial_carry if index == 0 else a[index - 1]
        circuit << pq.CNOT(a_bit, b_bit)
        circuit << pq.CNOT(a_bit, carry)
        circuit << pq.Toffoli(carry, b_bit, a_bit)


def _backward_pass(circuit, a, b, initial_carry):
    for index in range(len(a) - 1, -1, -1):
        carry = initial_carry if index == 0 else a[index - 1]
        circuit << pq.Toffoli(carry, b[index], a[index])
        circuit << pq.CNOT(a[index], carry)
        circuit << pq.CNOT(carry, b[index])


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n, a, b, carry_in, carry_out = _allocate_registers(num_state_qubits, kind)
    circuit = pq.QCircuit()
    _forward_pass(circuit, a, b, carry_in)
    if carry_out is not None:
        circuit << pq.CNOT(a[n - 1], carry_out)
    _backward_pass(circuit, a, b, carry_in)
    return circuit


atexit.register(lambda: machine.finalize())
