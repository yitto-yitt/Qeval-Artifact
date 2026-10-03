# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq
from qiskit.circuit.library import CDKMRippleCarryAdder
from qiskit import QuantumCircuit, transpile

machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):

    adder = CDKMRippleCarryAdder(num_state_qubits, kind)
    

    qc = QuantumCircuit(adder.num_qubits)
    qc.append(adder.to_instruction(), range(adder.num_qubits))
    

    qc_decomposed = transpile(qc, basis_gates=['cx', 'ccx'], optimization_level=0)
    

    pyqpanda_circuit = pq.QCircuit()
    
    for instruction in qc_decomposed.data:
        gate_name = instruction.operation.name
        qubits = instruction.qubits
        q_indices = [qc_decomposed.qubits.index(qubit) for qubit in qubits]
        
        if gate_name == 'cx':
            pyqpanda_circuit << pq.CNOT(global_qubits[q_indices[0]], global_qubits[q_indices[1]])
        elif gate_name == 'ccx':
            ctrl_qubits = pq.QVec()
            ctrl_qubits.append(global_qubits[q_indices[0]])
            ctrl_qubits.append(global_qubits[q_indices[1]])
            pyqpanda_circuit << pq.X(global_qubits[q_indices[2]]).control(ctrl_qubits)
            
    return pyqpanda_circuit


machine.finalize()

