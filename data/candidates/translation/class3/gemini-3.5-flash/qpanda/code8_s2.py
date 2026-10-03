# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq

def rx_gate(value=None):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    circuit = pq.QCircuit()
    
    var_cls = getattr(pq, 'var', getattr(pq, 'Var', None))
    
    if value is None:
        if var_cls is not None:
            theta = var_cls(0.0)
            circuit << pq.RX(q[0], theta)
        else:
            circuit << pq.RX(q[0], 0.0)
    else:
        circuit << pq.RX(q[0], value)
        
    return circuit
