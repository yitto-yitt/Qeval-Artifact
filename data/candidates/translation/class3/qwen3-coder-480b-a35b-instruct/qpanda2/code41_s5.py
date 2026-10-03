# EVAL_META: task_id=41, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
qubits = machine.qAlloc_many(3)

def compose_op():
    # Create 3-qubit identity operator
    id_op = pq.Operator(pq.QVec(qubits), pq.PauliOperator())
    
    # Create YX operator on 2 qubits
    yx_pauli = pq.PauliOperator({pq.QVec([qubits[0]]): 'Y', pq.QVec([qubits[1]]): 'X'})
    yx_op = pq.Operator(pq.QVec([qubits[0], qubits[1]]), yx_pauli)
    
    # Compose the operators - apply YX on qubits 0 and 2 of the identity
    composed_op = id_op.compose(yx_op, [0, 2])
    
    return composed_op

machine.finalize()
