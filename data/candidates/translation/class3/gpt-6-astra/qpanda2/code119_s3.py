# EVAL_META: task_id=119, framework=qpanda2, class=3
import atexit
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = operator.index(num_state_qubits)
    if n < 1:
        raise ValueError("num_state_qubits must be a positive integer.")
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'.")

    required = 2 * n + (1 if kind == "fixed" else 2)
    while len(qubits) < required:
        qubits.append(machine.qAlloc())

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

    circuit = pq.QCircuit()

    for i in range(n):
        previous_carry = carry if i == 0 else a[i - 1]
        circuit << pq.CNOT(a[i], b[i])
        circuit << pq.CNOT(a[i], previous_carry)
        circuit << pq.Toffoli(previous_carry, b[i], a[i])

    if carry_out is not None:
        circuit << pq.CNOT(a[-1], carry_out)

    for i in reversed(range(n)):
        previous_carry = carry if i == 0 else a[i - 1]
        circuit << pq.Toffoli(previous_carry, b[i], a[i])
        circuit << pq.CNOT(a[i], previous_carry)
        circuit << pq.CNOT(previous_carry, b[i])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(lambda: machine.finalize())
