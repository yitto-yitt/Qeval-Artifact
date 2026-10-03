# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, SWAP, S

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qc = QCircuit(3)
    qc << H(0)
    qc << SWAP(1, 2).control([0])
    qc << H(1)
    qc << S(0).dagger().control([1])
    return qc
