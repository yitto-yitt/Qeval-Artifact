# EVAL_META: task_id=84, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, U3

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    circuit = QCircuit()
    circuit << U3(q[1], 0.3, 0.2, 0.1).control(q[0])
    return circuit

machine.finalize()
