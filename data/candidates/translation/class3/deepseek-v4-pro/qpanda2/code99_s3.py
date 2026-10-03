# EVAL_META: task_id=99, framework=qpanda2, class=3
import numbers

from pyqpanda import CPUQVM, QCircuit

try:
    from pyqpanda import Parameter
except ImportError:
    Parameter = None

machine = CPUQVM()
machine.init()
q = machine.qAlloc_many(64)
c = machine.cAlloc_many(64)


def _is_unassigned_value(value):
    if isinstance(value, numbers.Real):
        return False
    if Parameter is not None and isinstance(value, Parameter):
        return True
    if hasattr(value, 'isBound') and not value.isBound():
        return True
    if hasattr(value, 'isUnBound') and value.isUnBound():
        return True
    return not isinstance(value, numbers.Real)


def _is_unassigned_parameterized_gate(gate):
    is_param_gate = False
    if hasattr(gate, 'isParameterGate'):
        is_param_gate = bool(gate.isParameterGate())

    try:
        params = gate.getParameter()
    except Exception:
        return False

    if params is None:
        return is_param_gate

    if isinstance(params, (list, tuple)):
        return any(_is_unassigned_value(p) for p in params)

    return _is_unassigned_value(params)


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()

    for gate in circuit:
        if not _is_unassigned_parameterized_gate(gate):
            new_circuit.insert(gate)

    return new_circuit


machine.finalize()
