# EVAL_META: task_id=0, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(30)

def create_quantum_circuit(n_qubits):
    return pq.QCircuit()

machine.finalize()
