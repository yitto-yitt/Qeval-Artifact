# EVAL_META: task_id=60, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(2)
def create_cy_gate():
    circuit = QCircuit()
    circuit << Sdag(q[1])
    circuit << CNOT(q[0], q[1])
    circuit << S(q[1])
    return circuit
machine.finalize()
