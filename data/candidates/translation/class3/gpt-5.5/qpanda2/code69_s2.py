# EVAL_META: task_id=69, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
atexit.register(machine.finalize)

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << S(q[1]).control([q[0]])
    circuit << H(q[1])
    circuit << S(q[0]).dagger().control([q[1]])
    return circuit
