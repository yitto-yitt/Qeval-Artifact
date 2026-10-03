# EVAL_META: task_id=1, framework=qpanda2, class=1
import pyqpanda
import builtins

def run_bell_state_simulator():
    qvm = pyqpanda.CPUQVM()
    qvm.init()
    q = qvm.qAlloc(2)
    c = qvm.cAlloc(2)
    
    prog = pyqpanda.QProg()
    prog << pyqpanda.H(q[0])
    prog << pyqpanda.CNOT(q[0], q[1])
    prog << pyqpanda.Measure(q[0], c[0])
    prog << pyqpanda.Measure(q[1], c[1])
    
    result = qvm.run_with_configuration(prog, c, 1000)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
