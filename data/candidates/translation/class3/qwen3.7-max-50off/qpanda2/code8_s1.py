# EVAL_META: task_id=8, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    circ = pq.QCircuit()
    if value is not None:
        circ << pq.RX(qubits[0], value)
    else:
        circ << pq.RX(qubits[0], 0.0)
    return circ

machine.finalize()
