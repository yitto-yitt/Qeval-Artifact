# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()
_keep = []

def inv_circuit(n):
    q = machine.qAlloc_many(n)
    _keep.append(q)
    qc = QCircuit()
    for i in range(2):
        qc << H(q[i + 1])
    for i in range(2):
        qc << CNOT(q[i + 1], q[i + 3])
    return qc.dagger()

if __name__ == "__main__":
    machine.finalize()
