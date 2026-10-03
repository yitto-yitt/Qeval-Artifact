# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
q = qvm.qAlloc_many(100)

def inv_circuit(n):
    circuit = QCircuit()
    circuit << CNOT(q[2], q[4])
    circuit << CNOT(q[1], q[3])
    circuit << H(q[2])
    circuit << H(q[1])
    return circuit

if __name__ == "__main__":
    qvm.finalize()
