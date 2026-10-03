# EVAL_META: task_id=0, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_allocated_qubits = []

def create_quantum_circuit(n_qubits):
    qubits = machine.qAlloc_many(n_qubits)
    _allocated_qubits.append(qubits)
    circ = pq.QCircuit()
    return circ

machine.finalize()
