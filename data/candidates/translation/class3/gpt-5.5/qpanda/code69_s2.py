# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    globals()["_pyqpanda3_task69_qvm"] = qvm
    globals()["_pyqpanda3_task69_qubits"] = q

    qc = QCircuit()
    qc << H(q[0])
    qc << S(q[1]).control([q[0]])
    qc << H(q[1])
    qc << S(q[0]).dagger().control([q[1]])
    return qc
