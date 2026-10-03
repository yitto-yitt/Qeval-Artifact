# EVAL_META: task_id=60, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_cy_gate():
    circ = pq.QCircuit()
    circ << pq.S(qubits[1]).dagger()
    circ << pq.CNOT(qubits[0], qubits[1])
    circ << pq.S(qubits[1])
    return circ

machine.finalize()
