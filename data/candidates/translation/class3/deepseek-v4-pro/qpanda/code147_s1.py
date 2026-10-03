# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, Y

def mcy(qc):
    controls = [qc.qubits[i] for i in range(4)]
    target = qc.qubits[4]
    gate = Y()
    for ctrl in controls:
        gate = gate.control(ctrl)
    qc.append(gate, controls + [target])
    return qc
