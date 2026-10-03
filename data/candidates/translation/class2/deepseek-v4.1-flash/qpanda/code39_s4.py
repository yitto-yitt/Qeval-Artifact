# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QCircuit, QProg, H


def create_uniform_superposition(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)

    circuit = QCircuit()
    for q in qubits:
        circuit << H(q)

    prog = QProg()
    prog << circuit

    for args in ((prog, qubits, 1000), (prog, 1000), (prog, qubits), (prog,)):
        try:
            qvm.run(*args)
            break
        except TypeError:
            continue
    else:
        raise RuntimeError("Failed to execute the quantum program on the CPUQVM.")

    for name in ("get_state_vector", "state_vector", "get_state",
                 "get_qstate", "getQState", "get_q_state",
                 "state", "statevector"):
        attr = getattr(qvm, name, None)
        if attr is None:
            continue
        if not callable(attr):
            return attr
        for call_args in ((), (prog,)):
            try:
                result = attr(*call_args)
            except TypeError:
                continue
            if result is not None:
                return result

    raise RuntimeError("Failed to retrieve the statevector from the CPUQVM.")
