# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

def and_gate(a, b):
    a &= 0b111
    b &= 0b111

    qa = QuantumRegister(3, 'a')
    qb = QuantumRegister(3, 'b')
    qc = QuantumRegister(3, 'c')
    cr = ClassicalRegister(3, 'result')
    circuit = QuantumCircuit(qa, qb, qc, cr)

    for i in range(3):
        if (a >> i) & 1:
            circuit.x(qa[i])
        if (b >> i) & 1:
            circuit.x(qb[i])

    for i in range(3):
        circuit.ccx(qa[i], qb[i], qc[i])

    circuit.measure(qc, cr)

    backend = AerSimulator()
    compiled = transpile(circuit, backend)
    result = backend.run(compiled, shots=1024).result()
    counts = result.get_counts()

    total = sum(counts.values())
    return {key: val / total for key, val in counts.items()}
