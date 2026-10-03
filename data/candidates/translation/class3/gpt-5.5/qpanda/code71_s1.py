# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_csx01_h1():
    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    qubits = machine.qAlloc_many(3)

    circuit = QCircuit()
    circuit << H(qubits[0])

    try:
        csx_gate = X1(qubits[1]).control([qubits[0]])
    except NameError:
        csx_gate = SX(qubits[1]).control([qubits[0]])

    circuit << csx_gate
    circuit << H(qubits[1])

    if not hasattr(create_quantum_circuit_based_h0_csx01_h1, "_resources"):
        create_quantum_circuit_based_h0_csx01_h1._resources = []
    create_quantum_circuit_based_h0_csx01_h1._resources.append((machine, qubits))

    return circuit
