# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def xor_gate(a, b):
    a &= 0xFF
    b &= 0xFF

    a_reg = QuantumRegister(8, 'a')
    b_reg = QuantumRegister(8, 'b')
    res_reg = QuantumRegister(8, 'res')
    c_reg = ClassicalRegister(8, 'out')

    qc = QuantumCircuit(a_reg, b_reg, res_reg, c_reg)

    for i in range(8):
        if (a >> i) & 1:
            qc.x(a_reg[i])
        if (b >> i) & 1:
            qc.x(b_reg[i])

    for i in range(8):
        qc.cx(a_reg[i], res_reg[i])
        qc.cx(b_reg[i], res_reg[i])

    qc.measure(res_reg, c_reg)

    backend = AerSimulator()
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts(qc)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
