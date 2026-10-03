# EVAL_META: task_id=70, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qc = QCircuit()
    qc.insert(H(q[0]))
    qc.insert(SWAP(q[1], q[2]).control(q[0]))
    qc.insert(H(q[1]))
    qc.insert(S(q[0]).dagger().control(q[1]))
    return qc

machine.finalize()
