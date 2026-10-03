# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import *

def calculate_stabilizer_state_info():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)

    prog = QProg()
    prog.insert(H(qubits[0]))
    prog.insert(CNOT(qubits[0], qubits[1]))

    state = machine.get_qstate(prog, qubits)
    machine.finalize()

    probabilities = {
        "00": float(abs(state[0]) ** 2),
        "01": float(abs(state[1]) ** 2),
        "10": float(abs(state[2]) ** 2),
        "11": float(abs(state[3]) ** 2),
    }
    return probabilities
