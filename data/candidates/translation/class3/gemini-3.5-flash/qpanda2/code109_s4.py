# EVAL_META: task_id=109, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def circuit():
    vqc = pq.VariationalQuantumCircuit()
    vqc.insert(pq.H(q[0]))
    theta = pq.Var(0.0)
    vqc.insert(pq.VariationalQuantumGate_RZ(q[0], theta))
    return vqc

machine.finalize()
