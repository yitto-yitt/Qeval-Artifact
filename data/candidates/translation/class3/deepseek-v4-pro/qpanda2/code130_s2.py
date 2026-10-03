# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()

def inv_circuit(n):
    q = machine.qAlloc_many(n)
    circuit = QCircuit()
    circuit << H(q[1])
    circuit << H(q[2])
    circuit << CNOT(q[1], q[3])
    circuit << CNOT(q[2], q[4])
    return circuit.dagger()

machine.finalize()
