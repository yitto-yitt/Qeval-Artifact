# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    qc = QuantumCircuit(16, 8)
    a_bits = format(a & 0xFF, '08b')
    b_bits = format(b & 0xFF, '08b')

    for i in range(8):
        if a_bits[7 - i] == '1':
            qc.x(i)
        if b_bits[7 - i] == '1':
            qc.x(8 + i)

    for i in range(8):
        qc.cx(i, 8 + i)
        qc.measure(8 + i, i)

    sim = AerSimulator()
    shots = 4096
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    dist = {}
    for key, val in counts.items():
        k = key.replace(' ', '')[-8:].zfill(8)
        dist[k] = dist.get(k, 0) + val / shots
    return dist
