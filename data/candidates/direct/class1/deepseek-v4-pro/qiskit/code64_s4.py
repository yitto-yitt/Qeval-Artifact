# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)

    # Apply Hadamard gates to the first n qubits
    qc.h(range(n))
    qc.barrier()

    # Simon oracle for hidden bitstring s
    # Copy input register to output register
    for i in range(n):
        qc.cx(i, i + n)

    if '1' in s:
        pivot = s.find('1')
        for j in range(n):
            if s[j] == '1':
                qc.cx(pivot, j + n)

    qc.barrier()

    # Apply Hadamard gates to the first n qubits again
    qc.h(range(n))
    qc.barrier()

    # Measure the first n qubits into classical register 'c'
    qc.measure(range(n), range(n))

    return qc
