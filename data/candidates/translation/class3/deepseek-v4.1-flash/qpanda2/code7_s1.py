# EVAL_META: task_id=7, framework=qpanda2, class=3
from pyqpanda import *
from pyqpanda import Var

qvm = CPUQVM()
qvm.init_qvm()
qubits = qAlloc_many(1)

def create_parametrized_gate():
    theta = Var("theta")
    circuit = QCircuit()
    circuit << RX(qubits[0], theta)
    return circuit

qvm.finalize()
