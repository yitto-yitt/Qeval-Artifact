# EVAL_META: task_id=4, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq

def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1],
                       [0, 0, 1, 0],
                       [1, 0, 0, 0],
                       [0, 1, 0, 0]], dtype=complex)

    try:
        circuit = pq.QCircuit()
    except TypeError:
        circuit = pq.QCircuit(2)

    if hasattr(pq, "QOracle"):
        for mat in (matrix, matrix.tolist()):
            try:
                gate = pq.QOracle([0, 1], mat)
                res = circuit << gate
                return circuit if res is None else res
            except Exception:
                pass

    try:
        res = circuit << pq.CNOT(1, 0)
        circuit = circuit if res is None else res
        res = circuit << pq.X(1)
        return circuit if res is None else res
    except Exception:
        qvm = pq.CPUQVM()
        if hasattr(qvm, "init_qvm"):
            qvm.init_qvm()
        qubits = qvm.qAlloc_many(2)
        try:
            circuit = pq.QCircuit()
        except TypeError:
            circuit = pq.QCircuit(2)
        res = circuit << pq.CNOT(qubits[1], qubits[0])
        circuit = circuit if res is None else res
        res = circuit << pq.X(qubits[1])
        return circuit if res is None else res
