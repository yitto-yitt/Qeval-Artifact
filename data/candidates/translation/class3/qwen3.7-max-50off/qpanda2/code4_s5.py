# EVAL_META: task_id=4, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=complex)
    circuit = pq.QCircuit()
    gate = pq.QUnitaryGate(matrix, [qubits[0], qubits[1]])
    circuit.insert(gate)
    return circuit

machine.finalize()
