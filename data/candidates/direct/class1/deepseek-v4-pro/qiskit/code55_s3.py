# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def or_gate(a, b):
    n = 3
    q_a = QuantumRegister(n, 'a')
    q_b = QuantumRegister(n, 'b')
    q_out = QuantumRegister(n, 'out')
    c_out = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q_a, q_b, q_out, c_out)

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    # Prepare input register states using little-endian qubit ordering.
    for i in range(n):
        if a_bits[n - 1 - i] == '1':
            qc.x(q_a[i])
        if b_bits[n - 1 - i] == '1':
            qc.x(q_b[i])

    # Reversible bitwise classical OR for each bit:
    # out = a XOR b XOR (a AND b) = a OR b
    for i in range(n):
        qc.cx(q_a[i], q_out[i])
        qc.cx(q_b[i], q_out[i])
        qc.ccx(q_a[i], q_b[i], q_out[i])

    qc.measure(q_out, c_out)

    simulator = AerSimulator()
    counts = simulator.run(qc, shots=1024).result().get_counts()
    total = sum(counts.values())

    return {state: count / total for state, count in counts.items()}
