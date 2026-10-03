# EVAL_META: task_id=70, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circuit = QCircuit()
    circuit << H(q[0]) << CSWAP(q[0], q[1], q[2]) << H(q[1]) << control(Sdg(q[0]), q[1])
    return circuit

machine.finalize()
