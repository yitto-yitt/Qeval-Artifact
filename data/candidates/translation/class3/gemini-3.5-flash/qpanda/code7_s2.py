# EVAL_META: task_id=7, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_parametrized_gate():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubit = qvm.qAlloc()
    theta = pq.var(0.0)
    vqc = pq.VariationalQuantumCircuit()
    vqc.insert(pq.VariationalQuantumGate_RX(qubit, theta))
    return vqc
