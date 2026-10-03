# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT


def calculate_stabilizer_state_info():
    prog = QProg()
    prog << H(0) << CNOT(0, 1)

    simulator = CPUQVM()
    simulator.run(prog)
    state = simulator.get_state_vector()

    return {
        format(index, "02b"): float(abs(amplitude) ** 2)
        for index, amplitude in enumerate(state)
        if abs(amplitude) ** 2 > 1e-15
    }
