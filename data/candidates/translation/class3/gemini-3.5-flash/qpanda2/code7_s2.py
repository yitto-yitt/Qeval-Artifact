# EVAL_META: task_id=7, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def create_parametrized_gate():
    theta = pq.var(0.0)
    vqc = pq.VariationalQuantumCircuit()
    vqc.insert(pq.VariationalQuantumGate_RX(qubits[0], theta))
    return vqc

machine.finalize()
