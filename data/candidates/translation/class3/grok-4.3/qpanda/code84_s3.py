# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, U3

def controlled_custom_unitary_circuit():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    circuit = QCircuit()
    custom_gate = U3(0.3, 0.2, 0.1, q[1]).control(q[0])
    circuit << custom_gate
    return circuit
