# EVAL_META: task_id=60, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_cy_gate():
    circuit = QCircuit()
    circuit.insert(S(q[1]).dagger())
    circuit.insert(CNOT(q[0], q[1]))
    circuit.insert(S(q[1]))
    return circuit

atexit.register(machine.finalize)
