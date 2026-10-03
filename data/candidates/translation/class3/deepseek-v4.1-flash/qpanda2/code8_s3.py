# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    var = Var("theta")
    circuit = VQCircuit()
    circuit << VQ_RX(qubits[0], var)
    if value is not None:
        var.set_value(value)
    return circuit
