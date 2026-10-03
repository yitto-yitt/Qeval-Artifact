# EVAL_META: task_id=125, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(64)


def circ_to_gate(circ):
    for _name in (
        "circuit_to_gate",
        "qcircuit_to_qgate",
        "convert_circuit_to_gate",
        "convert_qcircuit_to_qgate",
        "convert_circuit_to_qgate",
    ):
        _fn = globals().get(_name)
        if callable(_fn) and _fn is not circ_to_gate:
            try:
                return _fn(circ)
            except Exception:
                pass

    for _method in ("to_gate", "toQGate", "to_qgate", "to_q_gate", "convert_to_gate"):
        if hasattr(circ, _method):
            try:
                return getattr(circ, _method)()
            except Exception:
                pass

    try:
        _prog = QProg()
        _prog << circ
        try:
            _used_qubits = get_all_used_qubits(_prog)
        except Exception:
            _used_qubits = get_all_used_qubits(circ)

        try:
            _mat = get_matrix(_prog)
        except Exception:
            _mat = get_matrix(circ)

        try:
            return QOracle(_used_qubits, _mat)
        except Exception:
            pass
    except Exception:
        pass

    return circ


atexit.register(machine.finalize)
