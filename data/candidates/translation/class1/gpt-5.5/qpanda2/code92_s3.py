# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import *


def calculate_stabilizer_state_info():
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])

    probabilities_dict = prob_run_dict(prog, qubits, -1)

    destroy_quantum_machine(machine)
    return probabilities_dict
