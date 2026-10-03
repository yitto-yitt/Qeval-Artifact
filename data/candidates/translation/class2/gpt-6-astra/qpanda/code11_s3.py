# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg

def get_statevector(circuit):
    program = circuit if isinstance(circuit, QProg) else QProg()
    if program is not circuit:
        program << circuit

    simulator = CPUQVM()
    run_result = simulator.run(program, 1)
    result = getattr(simulator, "result", None)
    result = result() if callable(result) else result

    for source in (result, run_result, simulator):
        if source is None:
            continue
        for name in (
            "get_state_vector",
            "get_statevector",
            "get_qstate",
            "state_vector",
            "statevector",
        ):
            accessor = getattr(source, name, None)
            if accessor is not None:
                return accessor() if callable(accessor) else accessor

    raise RuntimeError("The simulator did not expose the resulting statevector.")
