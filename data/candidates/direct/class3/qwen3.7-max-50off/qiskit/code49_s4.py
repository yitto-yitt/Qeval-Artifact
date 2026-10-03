# EVAL_META: task_id=49, framework=qiskit, class=3
from qiskit import QuantumCircuit


def simple_elitzur_vaidman():
    """Return a simple Elitzur-Vaidman bomb tester circuit without measurements."""
    qc = QuantumCircuit(2)
    # First beam splitter: put photon into superposition of two paths
    qc.h(0)
    # Bomb interaction: CNOT with photon path as control, bomb as target
    qc.cx(0, 1)
    # Second beam splitter: recombine paths
    qc.h(0)
    return qc
