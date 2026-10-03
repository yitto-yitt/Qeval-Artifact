# EVAL_META: task_id=38, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    circ = QCircuit()
    circ << H(q[0])
    circ << CRZ(q[0], q[1], theta)
    circ << H(q[1])
    circ << CRY(q[1], q[0], theta)
    return circ

machine.finalize()
