# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H


def create_uniform_superposition(n):
    prog = QProg()
    for qubit in range(n):
        prog << H(qubit)

    simulator = CPUQVM()
    simulator.run(prog, 1)

    for source in (simulator, simulator.result()):
        for name in ("get_state_vector", "get_qstate", "state_vector"):
            accessor = getattr(source, name, None)
            if accessor is not None:
                return accessor() if callable(accessor) else accessor

    raise RuntimeError("The simulator did not expose its statevector.")
