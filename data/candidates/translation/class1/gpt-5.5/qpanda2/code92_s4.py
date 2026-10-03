# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import *


def calculate_stabilizer_state_info():
    machine = init_quantum_machine(QMachineType.CPU)
    try:
        qubits = machine.qAlloc_many(2)

        prog = QProg()
        prog.insert(H(qubits[0]))
        prog.insert(CNOT(qubits[0], qubits[1]))

        probabilities = prob_run_dict(prog, qubits, -1)
        return dict(probabilities)
    finally:
        destroy_quantum_machine(machine)
