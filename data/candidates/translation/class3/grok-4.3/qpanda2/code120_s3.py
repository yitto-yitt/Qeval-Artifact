# EVAL_META: task_id=120, framework=qpanda2, class=3
import pyqpanda as pq
import math
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
def create_diagonal_circuit(diag):
    n_qubits = int(math.log2(len(diag)))
    q = qubits[:n_qubits]
    circuit = pq.QCircuit()
    circuit << pq.DiagonalMatrix(q, diag)
    return circuit
machine.finalize()
