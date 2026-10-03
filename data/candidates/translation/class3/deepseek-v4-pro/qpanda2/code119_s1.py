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


def _majority_stage(a_bit, b_bit, carry_bit):
    stage = pq.QCircuit()
    stage << pq.CNOT(a_bit, b_bit)
    stage << pq.CNOT(a_bit, carry_bit)
    stage << pq.Toffoli(carry_bit, b_bit, a_bit)
    return stage


def _unmajority_stage(a_bit, b_bit, carry_bit):
    stage = pq.QCircuit()
    stage << pq.Toffoli(carry_bit, b_bit, a_bit)
    stage << pq.CNOT(a_bit, carry_bit)
    stage << pq.CNOT(carry_bit, b_bit)
    return stage


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n, a, b, carry_in, carry_out = _allocate_registers(num_state_qubits, kind)
    circuit = pq.QCircuit()
    for bit in range(n):
        carry = carry_in if bit == 0 else a[bit - 1]
        circuit << _majority_stage(a[bit], b[bit], carry)
    if carry_out is not None:
        circuit << pq.CNOT(a[n - 1], carry_out)
    for bit in range(n - 1, -1, -1):
        carry = carry_in if bit == 0 else a[bit - 1]
        circuit << _unmajority_stage(a[bit], b[bit], carry)
    return circuit


atexit.register(lambda: machine.finalize())
