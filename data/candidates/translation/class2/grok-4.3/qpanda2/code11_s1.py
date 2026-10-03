# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import *
def get_statevector(circuit):
    machine = init_quantum_machine(QMachineType.CPU)
    sv = get_state_vector(circuit, machine)
    return sv
