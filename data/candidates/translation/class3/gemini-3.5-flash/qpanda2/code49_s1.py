# EVAL_META: task_id=49, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def simple_elitzur_vaidman():
    circuit = pq.QCircuit()
    circuit << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.H(q[0])
    return circuit

machine.finalize()
