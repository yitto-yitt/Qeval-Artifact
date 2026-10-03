# EVAL_META: task_id=147, framework=qiskit, class=3
from qiskit.circuit.library import MCYGate


def mcy(qc):
    qc.append(MCYGate(num_ctrl_qubits=4), [0, 1, 2, 3, 4])
    return qc
