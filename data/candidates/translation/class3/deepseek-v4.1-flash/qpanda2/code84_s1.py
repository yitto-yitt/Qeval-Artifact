# EVAL_META: task_id=84, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    theta = 0.3
    phi = 0.2
    lam = 0.1
    alpha = (phi + lam) / 2.0

    circuit = QCircuit()

    # Controlled U3(theta, phi, lambda) with control qubits[0], target qubits[1]
    # U3 = e^{i*alpha} RZ(phi) RY(theta) RZ(lam)
    # Apply right-to-left: RZ(lam), RY(theta), RZ(phi), phase

    # Controlled RZ(lam)
    circuit << RZ(qubits[1], lam / 2.0)
    circuit << CNOT(qubits[0], qubits[1])
    circuit << RZ(qubits[1], -lam / 2.0)
    circuit << CNOT(qubits[0], qubits[1])

    # Controlled RY(theta)
    circuit << RY(qubits[1], theta / 2.0)
    circuit << CNOT(qubits[0], qubits[1])
    circuit << RY(qubits[1], -theta / 2.0)
    circuit << CNOT(qubits[0], qubits[1])

    # Controlled RZ(phi)
    circuit << RZ(qubits[1], phi / 2.0)
    circuit << CNOT(qubits[0], qubits[1])
    circuit << RZ(qubits[1], -phi / 2.0)
    circuit << CNOT(qubits[0], qubits[1])

    # Phase on control
    circuit << U1(qubits[0], alpha)

    return circuit

machine.finalize()
