# EVAL_META: task_id=59, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init()
qubits = machine.qAlloc_many(2)

def create_cz_gate():
    circ = pq.QCircuit()
    circ << pq.H(qubits[1])
    circ << pq.CNOT(qubits[0], qubits[1])
    circ << pq.H(qubits[1])
    return circ

machine.finalize()
