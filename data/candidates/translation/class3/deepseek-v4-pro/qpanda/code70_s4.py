# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    init(QuantumMachineType.CPU)
    q = qAlloc_many(3)
    circuit = QCircuit()
    circuit << H(q[0]) << CSWAP(q[0], q[1], q[2]) << H(q[1])
    circuit << Sdg(q[0]).control(q[1])
    return circuit
