# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
def inv_circuit(n):
    circuit = QCircuit()
    for i in range(2):
        circuit << H(qubits[i+1])
    for i in range(2):
        circuit << CNOT(qubits[i+1], qubits[i+3])
    return circuit.dagger()
machine.finalize()
