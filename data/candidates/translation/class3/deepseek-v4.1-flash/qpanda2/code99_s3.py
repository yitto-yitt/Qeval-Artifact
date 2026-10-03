# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *
from pyqpanda import var

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(10)

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    for node in circuit:
        if isinstance(node, QGate):
            if node.isParameterized():
                param = node.getParam()
                if isinstance(param, var):
                    continue
            new_circuit << node
        else:
            new_circuit << node
    return new_circuit

machine.finalize()
