# EVAL_META: task_id=4, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    circuit = pq.QCircuit()
    circuit.insert(pq.UnitaryMatrix(qubits, matrix))
    return circuit
