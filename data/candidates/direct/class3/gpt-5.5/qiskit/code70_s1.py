# EVAL_META: task_id=70, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import SGate


def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cswap(0, 1, 2)
    qc.h(1)
    qc.append(SGate().inverse().control(1), [1, 0])
    return qc
