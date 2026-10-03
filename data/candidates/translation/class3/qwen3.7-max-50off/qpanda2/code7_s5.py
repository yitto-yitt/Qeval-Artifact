# EVAL_META: task_id=7, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def create_parametrized_gate():
    theta = 0.0
    qc = pq.QCircuit()
    qc << pq.RX(qubits[0], theta)
    return qc

machine.finalize()
