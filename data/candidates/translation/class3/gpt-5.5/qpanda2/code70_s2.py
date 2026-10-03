# EVAL_META: task_id=70, framework=qpanda2, class=3
from math import pi
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circuit = QCircuit()
    circuit.insert(H(q[0]))
    circuit.insert(CNOT(q[2], q[1]))
    circuit.insert(Toffoli(q[0], q[1], q[2]))
    circuit.insert(CNOT(q[2], q[1]))
    circuit.insert(H(q[1]))
    circuit.insert(CR(q[1], q[0], -pi / 2))
    return circuit

machine.finalize()
