# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, U3

def controlled_custom_unitary_circuit():
    qc = QuantumCircuit()
    qubits = qc.qAlloc(2)
    custom_gate = U3(qubits[1], 0.3, 0.2, 0.1).control(qubits[0])
    qc << custom_gate
    return qc
