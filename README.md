# LADP Multi-Instance Claude Code Management System

## Overview

This project implements the LLM Autonomous Dialogue Protocol (LADP) v1.9 using multiple Claude Code instances managed through tmux. It enables coordinated multi-agent collaboration for complex tasks with built-in verification, role specialization, and structured communication.

## Key Features

- **Multi-Agent Coordination**: Run up to 5 Claude Code instances in parallel
- **LADP Protocol v1.9**: Implements formal communication protocol for LLM collaboration
- **Role-Based Architecture**: Supports Generator, Verifier, and Integrator agent roles
- **Structured Task Management**: Built-in reporting and progress tracking system
- **Token Management**: Efficient resource usage monitoring and optimization

## Prerequisites

- tmux (Terminal Multiplexer)
- Claude Code CLI installed and configured
- Unix-like environment (Linux/macOS/WSL)

## Quick Start

### 1. Prepare your task
Edit `instruction.md` and replace `"Specific task here"` at the bottom of the file with your actual task or objective.

### 2. Start tmux session
```bash
tmux
```

### 3. Launch Claude Code
```bash
claude --dangerously-skip-permissions
```
>[!WARNING]
>`--dangerously-skip-permissions` Use at your own risk!

### 4. Initialize the system (prompt)
```bash
following your instruction.md
```

## Project Structure

```
/
├── README.md          # This file
├── LADP.md            # LADP Protocol v1.9 specification
└── instruction.md     # Detailed multi-instance management manual
```

## Core Components

### LADP Protocol Implementation

The system implements LADP v1.9 with:
- **Chain-of-Verification**: Multi-step verification process for all generated content
- **Retrieval-Augmented Verification**: External knowledge grounding
- **Consensus Mechanism**: Weighted voting system with anomaly detection
- **Facilitation Phases**: DIVERGE → CONVERGE → DECIDE workflow

### Multi-Instance Management

- **Pane Configuration**: 5-pane tmux layout for parallel processing
- **Task Distribution**: Automated task assignment with progress tracking
- **Communication**: Inter-pane messaging using tmux send-keys
- **Health Monitoring**: Built-in health checks and recovery mechanisms

## Usage Examples

### Basic Task Assignment
```bash
tmux send-keys -t $PANE1 "You are pane1. [Task description]. Report completion with tmux send-keys -t $MAIN_PANE '[pane1] Task completed' Enter" Enter
```

### Parallel Processing Pipeline
```bash
# Data collection → Processing → Analysis → Report
# See instruction.md section 7.1 for detailed pipeline examples
```

### LADP Role Assignment
```bash
# Assign Generator, Verifier, and Integrator roles
# See instruction.md section 8.2 for role-based task distribution
```

## Best Practices

1. **Resource Management**
   - Monitor token usage with `ccusage` command
   - Clear context when exceeding 50k tokens
   - Use batch operations for efficiency

2. **Error Handling**
   - Implement timeout mechanisms for long-running tasks
   - Use health checks before critical operations
   - Maintain fallback strategies

3. **Task Organization**
   - Use clear naming conventions with pane IDs
   - Implement structured reporting formats
   - Track task dependencies explicitly

## Troubleshooting

### Common Issues

1. **Pane Not Responding**
   - Send Ctrl+C: `tmux send-keys -t $PANE C-c`
   - Clear and restart: `/clear` command

2. **Memory Issues**
   - Clear all panes simultaneously
   - Check system resources with `htop`

3. **Synchronization Problems**
   - Implement barrier synchronization (see instruction.md section 10.3)
   - Use completion markers in output

## Security Considerations

- The `--dangerously-skip-permissions` flag should only be used in development environments
- Avoid processing sensitive information across multiple panes
- Regularly clean up log files and temporary data

## Contributing

When contributing to this project:
1. Follow the LADP protocol specifications
2. Test multi-instance coordination thoroughly
3. Document any new patterns or utilities
4. Ensure backward compatibility with existing workflows

## License

This project follows the licensing terms of the LADP Protocol (CC-BY-SA 4.0) for protocol-related components.

## References

- [LADP Protocol v1.9 Specification](./LADP.md)
- [Multi-Instance Management Manual](./instruction.md)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
