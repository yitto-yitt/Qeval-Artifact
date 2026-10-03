# EVAL_META: task_id=8, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    if value is not None:
        circ = pq.QCircuit()
        circ << pq.RX(qubits[0], value)
        return circ
    else:
        try:
            theta = pq.Var("theta")
        except TypeError:
            theta = pq.Var()
        circ = pq.QCircuit()
        circ << pq.RX(qubits[0], theta)
        return circ

machine.finalize()
