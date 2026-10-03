# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
q = qvm.qAlloc_many(3)

def create_efficientSU2():
    vqc = VariationalQuantumCircuit()
    vqc.insert(BARRIER(q))
    for i in range(3):
        vqc.insert(RY(q[i], var(f"theta{i * 2}")))
        vqc.insert(RZ(q[i], var(f"theta{i * 2 + 1}")))
    vqc.insert(BARRIER(q))
    vqc.insert(CNOT(q[0], q[1]))
    vqc.insert(CNOT(q[0], q[2]))
    vqc.insert(CNOT(q[1], q[2]))
    vqc.insert(BARRIER(q))
    for i in range(3):
        vqc.insert(RY(q[i], var(f"theta{6 + i * 2}")))
        vqc.insert(RZ(q[i], var(f"theta{6 + i * 2 + 1}")))
    vqc.insert(BARRIER(q))
    return vqc

if __name__ == "__main__":
    qvm.finalize()
