# EVAL_META: task_id=109, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(1)

def circuit():
    vqc = pq.VariationalQuantumCircuit()
    vqc.insert(pq.VariationalQuantumGate_H(q[0]))
    vqc.insert(pq.VariationalQuantumGate_RZ(q[0], pq.var(0.0)))
    return vqc

machine.finalize()
