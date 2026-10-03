# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import QProg

try:
    from pyqpanda3.core import get_statevector as _get_sv
except ImportError:
    from pyqpanda3.core import get_qstate as _get_sv

def get_statevector(circuit):
    if isinstance(circuit, QProg):
        prog = circuit
    else:
        prog = QProg()
        prog << circuit
    return _get_sv(prog)
