# EVAL_META: task_id=38, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = qAlloc_many(2)
def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    circuit = QCircuit()
    circuit << H(q[0]) << CRZ(theta, q[0], q[1]) << H(q[1]) << CRY(theta, q[1], q[0])
    return circuit
machine.finalize()
