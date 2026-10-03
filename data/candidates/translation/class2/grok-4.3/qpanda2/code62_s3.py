# EVAL_META: task_id=62, framework=qpanda2, class=2
from pyqpanda import *
def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    machine = CPUQVM()
    machine.initQVM()
    qubits = machine.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for i in range(num_qubits):
        if state[i] == 1:
            circuit << X(qubits[i])
        if basis[i] == 1:
            circuit << H(qubits[i])
    return circuit
