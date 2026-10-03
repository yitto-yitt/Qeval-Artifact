# EVAL_META: task_id=3, framework=qiskit, class=2

from qiskit import QuantumCircuit

def create_ghz(drawing=False):
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.measure([0, 1, 2], [0, 1, 2])

    if drawing:
        fig = qc.draw('mpl')
        return qc, fig

    return qc
