# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    prog = QProg()
    target_circuit = QCircuit()
    target_circuit << X(q[1]) << H(q[2])
    controlled_circuit = target_circuit.control([q[0], q[3]])
    prog << controlled_circuit
    return prog

atexit.register(machine.finalize)
