# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def or_gate(a, b):
    # 9 qubits: 0-2 for a, 3-5 for b, 6-8 for result; 3 classical bits for result
    qc = QuantumCircuit(9, 3)

    # Initialize register a (qubits 0,1,2)
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)

    # Initialize register b (qubits 3,4,5)
    for i in range(3):
        if (b >> i) & 1:
            qc.x(3 + i)

    # Compute bitwise OR: result = a OR b
    # Using identity: a OR b = a XOR b XOR (a AND b)
    # CNOT a->r, CNOT b->r gives a XOR b
    # CCX(a,b,r) flips r when both a and b are 1, correcting the XOR to OR
    for i in range(3):
        a_q = i
        b_q = 3 + i
        r_q = 6 + i
        qc.cx(a_q, r_q)
        qc.cx(b_q, r_q)
        qc.ccx(a_q, b_q, r_q)

    # Measure result qubits into classical bits
    for i in range(3):
        qc.measure(6 + i, i)

    # Run on Aer simulator
    sim = AerSimulator()
    job = sim.run(qc, shots=1024)
    result = job.result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
