# EVAL_META: task_id=13, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QProg, U4

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def custom_rotation_gate():
    prog = QProg()
    prog << U4(qubits[0], np.pi / 2, np.pi / 2, np.pi / 2)
    return prog

if __name__ == "__main__":
    result = custom_rotation_gate()
    machine.directly_run(result)
    print(machine.get_qstate())
    machine.finalize()
