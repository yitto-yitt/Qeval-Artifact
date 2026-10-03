# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def and_gate(a, b):
    a_q = QuantumRegister(3, 'a')
    b_q = QuantumRegister(3, 'b')
    out_q = QuantumRegister(3, 'out')
    c = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(a_q, b_q, out_q, c)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(a_q[i])
        if (b >> i) & 1:
            qc.x(b_q[i])
        qc.ccx(a_q[i], b_q[i], out_q[i])

    for i in range(3):
        qc.measure(out_q[i], c[i])

    sim = AerSimulator()
    counts = sim.run(qc, shots=1024).result().get_counts(qc)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
