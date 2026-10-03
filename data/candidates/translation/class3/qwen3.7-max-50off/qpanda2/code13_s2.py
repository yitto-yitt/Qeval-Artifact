# EVAL_META: task_id=13, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def custom_rotation_gate():
    circuit = pq.QCircuit()
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    
    circuit << pq.RZ(qubits[0], lam)
    circuit << pq.RY(qubits[0], theta)
    circuit << pq.RZ(qubits[0], phi)
    
    return circuit

machine.finalize()
