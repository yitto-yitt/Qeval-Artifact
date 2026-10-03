# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()

def x_measurement(circuit, qubit, clbit):
    circuit << H(qubit) << Measure(qubit, clbit)
    return circuit

# Manual Cleanup
machine.finalize()
