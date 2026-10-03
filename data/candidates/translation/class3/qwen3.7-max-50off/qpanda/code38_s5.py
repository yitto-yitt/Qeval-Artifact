# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qc = QuantumCircuit(2)
    q = qc.qubits
    qc.h(q[0])
    qc.crz(theta, q[0], q[1])
    qc.h(q[1])
    qc.cry(theta, q[1], q[0])
    return qc
