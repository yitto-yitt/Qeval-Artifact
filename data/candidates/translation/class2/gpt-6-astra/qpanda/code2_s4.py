# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H, CNOT


def create_bell_statevector():
    simulator = CPUQVM()
    program = QProg()
    program << H(0) << CNOT(0, 1)
    simulator.run(program, 1)

    for source in (simulator.result(), simulator):
        for name in ("get_state_vector", "get_qstate", "get_statevector"):
            getter = getattr(source, name, None)
            if callable(getter):
                return getter()

    raise RuntimeError("The simulator does not expose its statevector.")
