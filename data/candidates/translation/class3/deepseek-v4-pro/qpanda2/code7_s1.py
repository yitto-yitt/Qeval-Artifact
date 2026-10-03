# EVAL_META: task_id=7, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def create_parametrized_gate():
    theta = pq.Variational(0.0, "theta")
    circuit = pq.QCircuit()
    circuit << pq.RX(q[0], theta)
    return circuit

machine.finalize()
