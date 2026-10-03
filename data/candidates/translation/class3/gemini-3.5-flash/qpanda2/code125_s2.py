# EVAL_META: task_id=125, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()

def circ_to_gate(circ):
    """
    In pyQPanda, a QCircuit itself acts as a composite gate. 
    It can be nested, controlled, and adjointed just like a QGate.
    """
    if isinstance(circ, pq.QProg):
        return pq.cast_qprog_to_qcircuit(circ)
    return circ

# Manual Cleanup
machine.finalize()
