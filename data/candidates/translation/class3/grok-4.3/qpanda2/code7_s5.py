# EVAL_META: task_id=7, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
def create_parametrized_gate():
    theta = Parameter("theta")
    quantum_circuit = QCircuit()
    quantum_circuit << RX(qubits[0], theta)
    return quantum_circuit
machine.finalize()
