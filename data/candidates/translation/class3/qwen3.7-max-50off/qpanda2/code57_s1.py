# EVAL_META: task_id=57, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_swap_gate():
    circ = pq.QCircuit()
    circ << pq.CNOT(qubits[0], qubits[1])
    circ << pq.CNOT(qubits[1], qubits[0])
    circ << pq.CNOT(qubits[0], qubits[1])
    return circ

machine.finalize()
