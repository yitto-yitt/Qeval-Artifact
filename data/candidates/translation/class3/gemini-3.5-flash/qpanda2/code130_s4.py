# EVAL_META: task_id=130, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

def inv_circuit(n):
    qubits = [global_qubits[i] for i in range(n)]
    circ = pq.QCircuit()
    circ << pq.H(qubits[1]) << pq.H(qubits[2])
    circ << pq.CNOT(qubits[1], qubits[3]) << pq.CNOT(qubits[2], qubits[4])
    return circ.dagger()

machine.finalize()
