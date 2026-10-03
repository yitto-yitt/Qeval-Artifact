# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg

def get_statevector(circuit):
    if isinstance(circuit, QProg):
        program = circuit
    else:
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
            "qstate",
        ):
            getter = getattr(source, name, None)
            if getter is not None:
                return getter() if callable(getter) else getter

    raise AttributeError("The simulator does not expose its statevector.")
