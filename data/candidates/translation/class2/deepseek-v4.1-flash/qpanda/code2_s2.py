# EVAL_META: task_id=2, framework=qpanda, class=2
from math import sqrt

from pyqpanda3.core import Statevector


def create_bell_statevector():
    return (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)
