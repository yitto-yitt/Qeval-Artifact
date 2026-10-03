# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    prog = QProg()
    prog << H(qubits[0])
    sx = X(qubits[1]).control(qubits[0])
    prog << RX(qubits[1], 0)
    prog << S(qubits[1])
    prog << H(qubits[1]).control(qubits[0])
    csx = QCircuit()
    csx << S(qubits[1]).control(qubits[0])
    csx << H(qubits[1]).control(qubits[0])
    csx << T(qubits[1]).control(qubits[0])
    csx << H(qubits[1]).control(qubits[0])
    qc = QCircuit()
    qc << H(qubits[0])
    qc << H(qubits[1]).control(qubits[0])
    qc << S(qubits[1]).control(qubits[0])
    qc << H(qubits[1]).control(qubits[0])
    qc << H(qubits[1])
    result = QProg()
    result << qc
    return result

machine.finalize()
