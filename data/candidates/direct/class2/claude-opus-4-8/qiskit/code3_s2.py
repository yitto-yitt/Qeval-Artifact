# EVAL_META: task_id=3, framework=qiskit, class=2
from qiskit import QuantumCircuit


def create_ghz(drawing=False):
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure(range(3), range(3))
    if drawing:
        fig = qc.draw(output="mpl")
        return qc, fig
    return qc
