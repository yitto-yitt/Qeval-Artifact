# EVAL_META: task_id=117, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def decompose_unitary(unitary):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    
    # Convert unitary to a 1D list of complex numbers
    flat_unitary = np.array(unitary).flatten().tolist()
    
    # Decompose the 2-qubit unitary matrix
    circuit = pq.matrix_decompose(qubits, flat_unitary)
    return circuit
