# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def or_gate(a, b):
    qc = QuantumCircuit(9, 3)
    # Initialize qubits for a (LSB at index 0)
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
    # Initialize qubits for b (LSB at index 3)
    for i in range(3):
        if (b >> i) & 1:
            qc.x(3 + i)
    # Compute bitwise OR into output qubits (indices 6,7,8)
    for i in range(3):
        aq = i
        bq = 3 + i
        oq = 6 + i
        qc.x(aq)
        qc.x(bq)
        qc.ccx(aq, bq, oq)
        qc.x(aq)
        qc.x(bq)
        qc.x(oq)
    # Measure output qubits to classical bits
    qc.measure([6, 7, 8], [0, 1, 2])
    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    job = simulator.run(compiled, shots=1024)
    counts = job.result().get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
