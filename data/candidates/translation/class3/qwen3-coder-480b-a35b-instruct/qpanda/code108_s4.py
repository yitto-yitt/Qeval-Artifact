# EVAL_META: task_id=108, framework=qpanda, class=3
import pyqpanda3.core as pq


def initialize_adjoint_and_compose(data1, data2):
    choi1 = pq.ChanOp(data1, pq.QVecType.UNITARY_MATRIX)
    choi2 = pq.ChanOp(data2, pq.QVecType.UNITARY_MATRIX)
    adjoint_choi1 = choi1.dagger()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
