# EVAL_META: task_id=57, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, CNOT

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_swap_gate():
    circuit = QCircuit()
    circuit << CNOT(q[0], q[1])
    circuit << CNOT(q[1], q[0])
    circuit << CNOT(q[0], q[1])
    return circuit

machine.finalize()
