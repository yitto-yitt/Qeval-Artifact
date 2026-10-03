# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H, CNOT


def create_bell_statevector():
    qvm = CPUQVM()
    prog = QProg()
    prog << H(0) << CNOT(0, 1)
    run_result = qvm.run(prog, 1)

    sources = [qvm, run_result]
    result_accessor = getattr(qvm, "result", None)
    if result_accessor is not None:
        sources.append(
            result_accessor() if callable(result_accessor) else result_accessor
        )

    for source in sources:
        if source is None:
            continue
        for name in (
            "get_statevector",
            "get_state_vector",
            "get_qstate",
            "statevector",
            "state_vector",
        ):
            accessor = getattr(source, name, None)
            if accessor is not None:
                return accessor() if callable(accessor) else accessor

    raise RuntimeError("The simulator did not expose its resulting statevector.")
