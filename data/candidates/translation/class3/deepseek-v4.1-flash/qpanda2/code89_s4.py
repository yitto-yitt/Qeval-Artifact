# EVAL_META: task_id=89, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_controlled_hgate():
    circuit = QCircuit()
    gate = H(q[2])
    gate.set_control([q[0], q[1]])
    circuit << gate
    return circuit

if __name__ == "__main__":
    machine.finalize()
