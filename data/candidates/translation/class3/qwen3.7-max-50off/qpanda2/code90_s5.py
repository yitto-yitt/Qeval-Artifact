# EVAL_META: task_id=90, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_custom_controlled():
    circ = pq.QCircuit()
    circ << pq.X(qubits[1]).control([qubits[0], qubits[3]])
    circ << pq.H(qubits[2]).control([qubits[0], qubits[3]])
    return circ

prog = pq.QProg()
prog << create_custom_controlled()

machine.finalize()
