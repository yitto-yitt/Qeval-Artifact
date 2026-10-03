# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg


def get_statevector(circuit):
    program = QProg()
    program << circuit

    simulator = CPUQVM()
    simulator.run(program, 1)

    for source in (simulator, simulator.result()):
        for name in (
            "get_state_vector",
            "get_statevector",
            "get_qstate",
            "state_vector",
            "statevector",
        ):
            accessor = getattr(source, name, None)
            if accessor is None:
                continue
            if not callable(accessor):
                return accessor
            try:
                return accessor()
            except TypeError:
                return accessor(program)

    raise RuntimeError("The simulator does not expose a statevector accessor.")
