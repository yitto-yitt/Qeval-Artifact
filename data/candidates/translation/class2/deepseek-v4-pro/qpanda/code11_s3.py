# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import QProg

def get_statevector(circuit):
    try:
        from pyqpanda3.core import StateVector
        if hasattr(StateVector, 'from_instruction'):
            return StateVector.from_instruction(circuit)
    except ImportError:
        pass

    qubits = circuit.get_used_qubits()
    if len(qubits) == 0:
        return [1.0 + 0.0j]

    qvm = None
    for method_name in ('get_origin_qvm', 'get_owner_qvm', 'get_qvm', 'get_owner'):
        if hasattr(qubits[0], method_name):
            qvm = getattr(qubits[0], method_name)()
            break
    if qvm is None:
        raise AttributeError("Could not obtain QVM from qubit")

    prog = QProg()
    prog << circuit
    return qvm.get_state(prog, qubits)
