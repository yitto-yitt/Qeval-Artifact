# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml

def circ_to_gate(circ):
    if isinstance(circ, qml.tape.QuantumTape):
        ops = circ.operations
        wires = circ.wires
        
        class CircuitGate(qml.operation.Operation):
            num_wires = len(wires)
            
            @staticmethod
            def compute_decomposition(*params, wires=None):
                return ops
                
        return CircuitGate
    
    try:
        return qml.from_qiskit(circ)
    except Exception:
        return circ
