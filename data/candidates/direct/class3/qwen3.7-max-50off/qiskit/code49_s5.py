# EVAL_META: task_id=49, framework=qiskit, class=3
from qiskit import QuantumCircuit


def simple_elitzur_vaidman():
    qc = QuantumCircuit(2)
    # First beam splitter: put photon in superposition of paths
    qc.h(0)
    # Bomb interaction: CNOT represents live bomb detector
    # If photon takes path |1>, bomb qubit flips (interaction/explode)
    qc.cx(0, 1)
    # Second beam splitter: recombine paths
    qc.h(0)
    return qc
