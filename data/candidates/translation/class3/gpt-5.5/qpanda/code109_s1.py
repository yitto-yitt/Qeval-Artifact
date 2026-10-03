# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *

def circuit():
    qvm = CPUQVM()
    for _init_name in ("init_qvm", "init"):
        if hasattr(qvm, _init_name):
            try:
                getattr(qvm, _init_name)()
                break
            except TypeError:
                pass

    q = qvm.qAlloc_many(1)
    qc = QCircuit()

    theta = None
    for _param_name in ("Parameter", "QParameter"):
        if _param_name in globals():
            try:
                theta = globals()[_param_name]("th")
                break
            except Exception:
                pass

    if theta is None and "var" in globals():
        try:
            theta = var(0.0)
        except Exception:
            theta = None

    if theta is None and "Variable" in globals():
        try:
            theta = Variable(0.0)
        except Exception:
            theta = None

    if theta is None:
        theta = 0.0

    qc << H(q[0])

    try:
        qc << RZ(q[0], theta)
    except TypeError:
        qc << RZ(theta, q[0])

    try:
        qc._qvm = qvm
    except Exception:
        pass

    return qc
