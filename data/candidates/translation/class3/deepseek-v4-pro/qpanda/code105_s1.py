# EVAL_META: task_id=105, framework=qpanda, class=3
import pyqpanda3 as pq

def initialize_cnot_dihedral():
    qv = pq.QVec(2)  # create a vector of 2 qubits
    circuit = pq.QCircuit()
    circuit << pq.CNOT(qv[0], qv[1]) << pq.T(qv[0])
    return circuit
