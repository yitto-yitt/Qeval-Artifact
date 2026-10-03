# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qvm = CPUQVM()
    qvm.initQVM()
    q = qvm.qAllocMany(3)
    circuit = QCircuit()
    circuit << H(q[0]) << CSWAP(q[0], q[1], q[2]) << H(q[1]) << CS(q[1], q[0]).dagger()
    return circuit
