# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(10)
def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    if hasattr(circuit, 'data'):
        for instruction in circuit.data:
            instr = instruction
            if not (isinstance(getattr(instr, 'params', None), Parameter) or 
                    (hasattr(instr, 'params') and len(instr.params) > 0 and isinstance(instr.params[0], Parameter))):
                new_circuit.append(instr)
    else:
        new_circuit = circuit
    return new_circuit
machine.finalize()
