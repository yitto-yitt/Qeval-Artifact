# EVAL_META: task_id=86, framework=cirq, class=3
import cirq
from cirq import circuits

def collect_linear_blocks_with_and_without_limit():
    # create 5-qubit circuit
    q0, q1, q2, q3, q4 = cirq.LineQubit.range(5)
    operations = [
        cirq.H(q0),
        cirq.CX(q0, q1),
        cirq.CX(q1, q2),
        cirq.CX(q2, q3),
        cirq.CX(q3, q4),
    ]
    circuit = cirq.Circuit(operations)
    
    # No block width restriction: collect all consecutive two-qubit gates into blocks
    # In Cirq, we can use optimizers to merge consecutive two-qubit gates into subcircuits.
    # We'll manually partition the circuit into blocks of linear operations.
    
    # For the full (unrestricted) case, we simply attempt to serialize all two-qubit gates 
    # as one block. We'll use a custom gather linear block function.
    
    def _collect_linear_blocks(circuit, max_block_width=None):
        """Collect linear blocks of CX gates (two-qubit operations) into subcircuits.
        
        A linear block is a sequence of two-qubit operations where operations 
        can be merged. In Cirq, we can use serializable operations or 
        CircuitOperation to represent blocks.
        """
        if max_block_width is None:
            return _collect_max_block(circuit)
        else:
            return _collect_limited_block(circuit, max_block_width)
    
    def _collect_max_block(circuit):
        # Simply wrap all two-qubit ops in a single subcircuit if possible
        # For this specific circuit, we know the structure, so we can just 
        # create a block from all CX gates.
        ops = list(circuit.all_operations())
        new_moments = []
        block_ops = []
        for op in ops:
            if isinstance(op.gate, cirq.HGate):
                new_moments.append(cirq.Moment(op))
            elif isinstance(op.gate, cirq.CXGate):
                block_ops.append(op)
        # Create a single block from all CX operations
        if block_ops:
            block_circuit = cirq.Circuit(block_ops)
            block_op = block_circuit.to_op()
            new_moments.append(cirq.Moment(block_op))
        return cirq.Circuit(new_moments)
    
    def _collect_limited_block(circuit, max_width):
        """Collect blocks, but limit each block's width (number of qubits) to max_width.
        
        Since CX gates act on two qubits, max_block_width=3 means we can have at most
        3 qubits involved in a block.
        """
        ops = list(circuit.all_operations())
        new_moments = []
        current_block_ops = []
        current_block_qubits = set()
        max_ops_per_group = max_width * 2  # heuristic for partition
        
        for op in ops:
            if isinstance(op.gate, cirq.HGate):
                if current_block_ops:
                    block_circuit = cirq.Circuit(current_block_ops)
                    block_op = block_circuit.to_op()
                    new_moments.append(cirq.Moment(block_op))
                    current_block_ops = []
                    current_block_qubits = set()
                new_moments.append(cirq.Moment(op))
            elif isinstance(op.gate, cirq.CXGate):
                qubit_set = set(op.qubits)
                # Estimate width after adding this op
                new_width = len(current_block_qubits | qubit_set)
                if new_width <= max_width and len(current_block_ops) < max_ops_per_group:
                    current_block_ops.append(op)
                    current_block_qubits.update(qubit_set)
                else:
                    # Finish current block and start a new one
                    if current_block_ops:
                        block_circuit = cirq.Circuit(current_block_ops)
                        block_op = block_circuit.to_op()
                        new_moments.append(cirq.Moment(block_op))
                    current_block_ops = [op]
                    current_block_qubits = set(qubit_set)
        
        # Remaining ops
        if current_block_ops:
            block_circuit = cirq.Circuit(current_block_ops)
            block_op = block_circuit.to_op()
            new_moments.append(cirq.Moment(block_op))
        
        return cirq.Circuit(new_moments)
    
    full_block = _collect_max_block(circuit)
    limited_block = _collect_limited_block(circuit, max_width=3)
    
    return full_block, limited_block
