# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, CSX

def create_quantum_circuit_based_h0_csx01_h1():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    circuit = QCircuit()
    circuit << H(q[0]) << CSX(q[0], q[1]) << H(q[1])
    return circuit
