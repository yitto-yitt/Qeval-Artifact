# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(5)
def inv_circuit(n):
    circuit = QCircuit()
    for i in range(2):
        circuit << H(qubits[i+1])
    for i in range(2):
        circuit << CNOT(qubits[i+1], qubits[i+3])
    return circuit.dagger()
machine.finalize()
