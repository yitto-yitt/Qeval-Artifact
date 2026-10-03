# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H


def create_uniform_superposition(n):
    prog = QProg()
    for qubit in range(n):
        prog << H(qubit)

    qvm = CPUQVM()
    qvm.run(prog, 1)

    for source in (qvm, qvm.result()):
        for name in ("get_state_vector", "get_statevector", "get_qstate"):
            getter = getattr(source, name, None)
            if callable(getter):
                return getter()

    raise RuntimeError("The simulator does not expose its resulting statevector.")
