# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H, CNOT


def create_bell_statevector():
    qvm = CPUQVM()
    program = QProg()
    program << H(0) << CNOT(0, 1)
    qvm.run(program, 1)

    for source in (qvm, qvm.result()):
        for name in ("get_state_vector", "get_statevector", "get_qstate"):
            getter = getattr(source, name, None)
            if callable(getter):
                return getter()

    raise RuntimeError("The simulator does not expose its statevector.")
