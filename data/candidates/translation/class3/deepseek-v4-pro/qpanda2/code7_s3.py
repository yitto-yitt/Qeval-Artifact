# EVAL_META: task_id=7, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(1)

def create_parametrized_gate():
    theta = var(0.0, "theta")
    circuit = VariationalQuantumCircuit()
    circuit.insert(VariationalQuantumGate_RX(q[0], theta))
    return circuit

machine.finalize()
