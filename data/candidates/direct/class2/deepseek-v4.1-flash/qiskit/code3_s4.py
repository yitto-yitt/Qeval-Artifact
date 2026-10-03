# EVAL_META: task_id=3, framework=qiskit, class=2
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def create_ghz(drawing=False):
    qr = QuantumRegister(3, 'q')
    cr = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(qr, cr)

    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])
    qc.measure(qr, cr)

    if drawing:
        return qc, qc.draw('mpl')
    return qc
