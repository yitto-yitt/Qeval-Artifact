# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg

def get_statevector(circuit):
    program = circuit
    if not isinstance(circuit, QProg):
        program = QProg()
        program << circuit

    simulator = CPUQVM()
    execution_result = simulator.run(program, 1)

    sources = [simulator, execution_result]
    result_accessor = getattr(simulator, "result", None)
    if result_accessor is not None:
        sources.append(
            result_accessor() if callable(result_accessor) else result_accessor
        )

    for source in sources:
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

    raise RuntimeError("The simulator did not expose its resulting statevector.")
