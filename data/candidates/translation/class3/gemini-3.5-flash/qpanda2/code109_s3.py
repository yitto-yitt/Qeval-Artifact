# EVAL_META: task_id=109, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def circuit():
    vqc = pq.VariationalQuantumCircuit()
    theta = pq.var(0.0)
    vqc.insert(pq.VariationalQuantumGate_H(q[0]))
    vqc.insert(pq.VariationalQuantumGate_RZ(q[0], theta))
    return vqc

# Manual Cleanup
machine.finalize()
