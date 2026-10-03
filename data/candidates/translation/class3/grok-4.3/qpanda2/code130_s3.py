# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(10)
def inv_circuit(n):
    circuit = QCircuit()
    for i in range(2):
        circuit << H(q[i+1])
    for i in range(2):
        circuit << CNOT(q[i+1], q[i+3])
    return circuit.dagger()
machine.finalize()
