# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H

def create_uniform_superposition(n):
    prog = QProg()
    for qubit in range(n):
        prog << H(qubit)

    simulator = CPUQVM()
    execution_result = simulator.run(prog, 1)

    result = getattr(simulator, "result", None)
    if callable(result):
        result = result()

    for source in (result, execution_result, simulator):
        if source is None:
            continue
        for name in (
            "get_state_vector",
            "get_statevector",
            "get_qstate",
            "state_vector",
            "statevector",
        ):
            state = getattr(source, name, None)
            if state is not None:
                return state() if callable(state) else state

    raise RuntimeError("The simulator did not expose its resulting statevector.")
