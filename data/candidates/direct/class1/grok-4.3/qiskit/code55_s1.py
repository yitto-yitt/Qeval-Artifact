# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def or_gate(a, b):
    a_reg = QuantumRegister(3, 'a')
    b_reg = QuantumRegister(3, 'b')
    out_reg = QuantumRegister(3, 'out')
    c_reg = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(a_reg, b_reg, out_reg, c_reg)
    for i in range(3):
        if (a >> i) & 1:
            qc.x(a_reg[i])
        if (b >> i) & 1:
            qc.x(b_reg[i])
    for i in range(3):
        qc.cx(a_reg[i], out_reg[i])
        qc.cx(b_reg[i], out_reg[i])
        qc.ccx(a_reg[i], b_reg[i], out_reg[i])
    qc.measure(out_reg, c_reg)
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}
    return probs
