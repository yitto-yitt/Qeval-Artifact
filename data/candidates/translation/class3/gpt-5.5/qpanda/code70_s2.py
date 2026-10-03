# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import *


def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circuit = QCircuit()

    circuit << H(0)
    circuit << SWAP(1, 2).control([0])
    circuit << H(1)
    circuit << S(0).dagger().control([1])

    return circuit
