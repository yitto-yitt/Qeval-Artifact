# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg

def get_statevector(circuit):
    program = circuit
    if not isinstance(program, QProg):
        program = QProg()
        program << circuit

    simulator = CPUQVM()
    simulator.run(program, 1)

    for name in ("get_statevector", "get_state_vector", "get_qstate"):
        getter = getattr(simulator, name, None)
        if callable(getter):
            return getter()

    result = simulator.result()
    for name in ("get_statevector", "get_state_vector", "get_qstate"):
        getter = getattr(result, name, None)
        if callable(getter):
            return getter()

    raise AttributeError("The simulator does not expose a statevector accessor.")
