# EVAL_META: task_id=84, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(2)
def controlled_custom_unitary_circuit():
    circuit = QCircuit()
    u3_gate = U3(0.3, 0.2, 0.1, qubits[1])
    controlled_gate = u3_gate.control(qubits[0])
    circuit << controlled_gate
    return circuit
machine.finalize()
