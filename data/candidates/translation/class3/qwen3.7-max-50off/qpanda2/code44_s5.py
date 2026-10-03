# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    circ = pq.QCircuit()
    circ << pq.CRY(qubits[0], qubits[1], 0.2)
    circ << pq.X(qubits[2])
    return circ

res = tensor_circuits()
machine.finalize()
