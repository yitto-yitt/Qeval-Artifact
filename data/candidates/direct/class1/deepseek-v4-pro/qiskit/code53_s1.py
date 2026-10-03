# EVAL_META: task_id=53, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def xor_gate(a, b):
    qa = QuantumRegister(8, 'a')
    qb = QuantumRegister(8, 'b')
    qres = QuantumRegister(8, 'res')
    creg = ClassicalRegister(8, 'meas')
    circuit = QuantumCircuit(qa, qb, qres, creg)

    for i in range(8):
        if (a >> i) & 1:
            circuit.x(qa[i])
        if (b >> i) & 1:
            circuit.x(qb[i])

    for i in range(8):
        circuit.cx(qa[i], qres[i])
        circuit.cx(qb[i], qres[i])

    circuit.measure(qres, creg)

    backend = AerSimulator()
    job = backend.run(circuit, shots=1024)
    counts = job.result().get_counts()

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
