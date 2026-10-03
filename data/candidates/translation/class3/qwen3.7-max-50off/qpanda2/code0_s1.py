# EVAL_META: task_id=0, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init()

def create_quantum_circuit(n_qubits):
    qubits = machine.qAlloc_many(n_qubits)
    qc = pq.QCircuit()
    return qc

machine.finalize()
