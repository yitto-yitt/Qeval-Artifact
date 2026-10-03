# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qc = QuantumCircuit(3)
    q = qc.qubits
    qc.h(q[0])
    qc.cswap(q[0], q[1], q[2])
    qc.h(q[1])
    qc.csdg(q[1], q[0])
    return qc
