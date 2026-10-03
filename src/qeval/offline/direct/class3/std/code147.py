# EVAL_META: task_id=147, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.circuit.library import YGate

def mcy(qc):
    mcy_gate = YGate().control(num_ctrl_qubits=4)
    qc.append(mcy_gate, range(5))
    return qc


# ==================================================
