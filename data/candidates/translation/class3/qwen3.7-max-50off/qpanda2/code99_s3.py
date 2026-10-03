# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda

machine = pyqpanda.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
cbits = machine.cAlloc_many(10)

def remove_unassigned_parameterized_gates(circuit):
    qc = pyqpanda.QCircuit()
    if hasattr(circuit, 'data'):
        for instruction in circuit.data:
            instr = instruction.operation if hasattr(instruction, 'operation') else instruction[0]
            has_param = False
            if hasattr(instr, 'params'):
                params = instr.params if isinstance(instr.params, list) else [instr.params]
                for p in params:
                    if type(p).__name__ in ['Parameter', 'Var', 'ParameterExpression']:
                        has_param = True
                        break
            if not has_param:
                if hasattr(qc, 'append'):
                    qc.append(instruction)
    return qc

machine.finalize()
