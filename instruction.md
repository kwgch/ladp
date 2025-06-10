# Claude Code Multi-Instance Management Manual

## 1. Introduction

This manual is a guide for efficiently managing and operating multiple Claude Code instances using tmux.

## 2. Initial Setup

### 2.1 Creating tmux Pane Configuration

```bash
# Record current directory
WORK_DIR=$(pwd)

# Split into 5 panes (more stable method)
tmux split-window -h
tmux split-window -v
tmux select-pane -t 0
tmux split-window -v
tmux select-pane -t 2
tmux split-window -v

# Adjust layout evenly
tmux select-layout tiled
```

### 2.2 Confirming and Recording Pane IDs

```bash
# Confirm all pane IDs
tmux list-panes -F "#{pane_index}: %#{pane_id}"

# Save results to variables (example)
MAIN_PANE=%33
PANE1=%34
PANE2=%35
PANE3=%36
PANE4=%37
```

### 2.3 Starting Claude Code

```bash
# Alias setup (first time only)
alias cc="claude --dangerously-skip-permissions"

# Parallel startup in all panes (replace with actual pane IDs)
for pane in $PANE1 $PANE2 $PANE3 $PANE4; do
    tmux send-keys -t $pane "cd '$WORK_DIR' && cc" && sleep 0.1 && tmux send-keys -t $pane Enter &
done
wait

# Startup verification (after 10 seconds wait)
sleep 10
for pane in $PANE1 $PANE2 $PANE3 $PANE4; do
    echo "=== $pane status ==="
    tmux capture-pane -t $pane -p | tail -3
done
```

## 3. Task Management System

### 3.1 Task Assignment Templates

#### Basic Form
```bash
tmux send-keys -t $PANE1 "cd '$WORK_DIR' && You are pane1. [Task content]. After completion, report with tmux send-keys -t $MAIN_PANE '[pane1] Task completed' && sleep 0.1 && tmux send-keys -t $MAIN_PANE Enter." && sleep 0.1 && tmux send-keys -t $PANE1 Enter
```

#### For Complex Tasks (including line breaks)
```bash
tmux send-keys -t $PANE1 "cd '$WORK_DIR' && \\
You are pane1. Please execute the following tasks: \\
1. [Task 1] \\
2. [Task 2] \\
3. [Task 3] \\
Please report progress at each step completion. \\
Reporting method: tmux send-keys -t $MAIN_PANE '[pane1] Progress: [content]' && sleep 0.1 && tmux send-keys -t $MAIN_PANE Enter" && sleep 0.1 && tmux send-keys -t $PANE1 Enter
```

### 3.2 Parallel Task Execution

```bash
# Assign different tasks to each pane
tmux send-keys -t $PANE1 "You are pane1. Please handle data collection. After completion, report with tmux send-keys -t $MAIN_PANE '[pane1] Data collection completed' && sleep 0.1 && tmux send-keys -t $MAIN_PANE Enter." && sleep 0.1 && tmux send-keys -t $PANE1 Enter & \
tmux send-keys -t $PANE2 "You are pane2. Please handle data analysis. After completion, report with tmux send-keys -t $MAIN_PANE '[pane2] Analysis completed' && sleep 0.1 && tmux send-keys -t $MAIN_PANE Enter." && sleep 0.1 && tmux send-keys -t $PANE2 Enter & \
tmux send-keys -t $PANE3 "You are pane3. Please handle report creation. After completion, report with tmux send-keys -t $MAIN_PANE '[pane3] Report completed' && sleep 0.1 && tmux send-keys -t $MAIN_PANE Enter." && sleep 0.1 && tmux send-keys -t $PANE3 Enter & \
wait
```

## 4. Communication System (Report, Contact, Consultation)

### 4.1 Report Format

```bash
# Basic report
[pane_number] Status: Message

# Examples
[pane1] Completed: Data collection finished
[pane2] Error: File not found
[pane3] Progress: 50% complete, approximately 10 minutes remaining
[pane4] Consultation: May I change the approach?
```

### 4.2 Regular Reporting Mechanism

```bash
# For long-running tasks, incorporate regular reporting
tmux send-keys -t $PANE1 "You are pane1. Starting large-scale data processing. \\
Please report progress every 10 minutes: \\
tmux send-keys -t $MAIN_PANE '[pane1] Progress: XX% complete' && sleep 0.1 && tmux send-keys -t $MAIN_PANE Enter" && sleep 0.1 && tmux send-keys -t $PANE1 Enter
```

## 5. Token Management

### 5.1 Usage Monitoring

```bash
# Check token usage for each pane
for pane in $PANE1 $PANE2 $PANE3 $PANE4; do
    echo "=== Checking $pane ==="
    tmux send-keys -t $pane "ccusage" && sleep 0.1 && tmux send-keys -t $pane Enter
    sleep 2
    tmux capture-pane -t $pane -p | grep -A5 "Token"
done
```

### 5.2 Efficient Clear Strategy

```bash
# Conditional clear
check_and_clear() {
    local pane=$1
    local threshold=50000  # Token threshold
    
    # Check usage and determine if clear is needed
    tmux send-keys -t $pane "ccusage" && sleep 0.1 && tmux send-keys -t $pane Enter
    sleep 2
    
    # Clear if threshold exceeded
    tmux send-keys -t $pane "/clear" && sleep 0.1 && tmux send-keys -t $pane Enter
}

# Batch clear all panes (after task completion)
for pane in $PANE1 $PANE2 $PANE3 $PANE4; do
    tmux send-keys -t $pane "/clear" && sleep 0.1 && tmux send-keys -t $pane Enter &
done
wait
```

## 6. Status Monitoring and Troubleshooting

### 6.1 Health Check

```bash
# Check status of all panes
health_check() {
    for pane in $PANE1 $PANE2 $PANE3 $PANE4; do
        echo "=== $pane Health Check ==="
        
        # Check latest output
        local last_output=$(tmux capture-pane -t $pane -p | tail -5)
        
        # Responsiveness check
        tmux send-keys -t $pane "echo 'Health check OK'" && sleep 0.1 && tmux send-keys -t $pane Enter
        sleep 2
        
        # Error pattern detection
        if echo "$last_output" | grep -q "error\|Error\|ERROR"; then
            echo "WARNING: Error detected in $pane"
        fi
    done
}
```

### 6.2 Problem Resolution Procedures

```bash
# When a pane freezes
recover_pane() {
    local pane=$1
    
    # 1. Send Ctrl+C
    tmux send-keys -t $pane C-c
    sleep 1
    
    # 2. Clear command
    tmux send-keys -t $pane "/clear" && sleep 0.1 && tmux send-keys -t $pane Enter
    sleep 1
    
    # 3. Assign new task
    tmux send-keys -t $pane "echo 'Recovered and ready'" && sleep 0.1 && tmux send-keys -t $pane Enter
}
```

## 7. Advanced Coordination Patterns

### 7.1 Pipeline Processing

```bash
# Data processing pipeline
# Pane1: Data collection → Pane2: Preprocessing → Pane3: Analysis → Pane4: Report generation

# Step 1: Data collection
tmux send-keys -t $PANE1 "You are pane1. Please collect data and save to data.json. After completion, report with tmux send-keys -t $MAIN_PANE '[pane1] Data collection completed, ready for handoff to pane2' && sleep 0.1 && tmux send-keys -t $MAIN_PANE Enter." && sleep 0.1 && tmux send-keys -t $PANE1 Enter

# After waiting for completion, proceed to Step 2
# (Execute after confirmation in main pane)
tmux send-keys -t $PANE2 "You are pane2. Please preprocess data.json and create processed_data.json..." && sleep 0.1 && tmux send-keys -t $PANE2 Enter
```

### 7.2 Collaborative Work

```bash
# Collaborative editing with multiple panes
# Give all panes access to the same file, edit different sections

tmux send-keys -t $PANE1 "You are pane1. Please create the Introduction section of report.md. Be careful not to conflict with other panes." && sleep 0.1 && tmux send-keys -t $PANE1 Enter & \
tmux send-keys -t $PANE2 "You are pane2. Please create the Methodology section of report.md." && sleep 0.1 && tmux send-keys -t $PANE2 Enter & \
tmux send-keys -t $PANE3 "You are pane3. Please create the Results section of report.md." && sleep 0.1 && tmux send-keys -t $PANE3 Enter & \
wait
```

## 8. LADP Protocol Implementation Examples

### 8.1 Protocol Understanding Phase

```bash
# Have all panes understand the LADP protocol
for i in 1 2 3 4; do
    pane_var="PANE$i"
    pane_id=${!pane_var}
    tmux send-keys -t $pane_id "cd '$WORK_DIR' && You are pane${i}. Please read LADP.md and understand the LADP protocol v1.9. After reading, report with tmux send-keys -t $MAIN_PANE '[pane${i}] LADP understanding complete' && sleep 0.1 && tmux send-keys -t $MAIN_PANE Enter." && sleep 0.1 && tmux send-keys -t $pane_id Enter &
done
wait
```

### 8.2 Role Assignment

```bash
# Assign Generator, Verifier, Integrator roles
tmux send-keys -t $PANE1 "You are Generator Agent (pane1). Please generate creative ideas about unexpected fusion of cross-disciplinary knowledge. Output proposals in (synthesis) format according to the LADP protocol." && sleep 0.1 && tmux send-keys -t $PANE1 Enter

tmux send-keys -t $PANE2 "You are Verifier Agent (pane2). Please verify proposals from other agents. Output results in (verify) format of the LADP protocol." && sleep 0.1 && tmux send-keys -t $PANE2 Enter

tmux send-keys -t $PANE3 "You are Integrator Agent (pane3). Please integrate verified proposals. Output in (integration) format of the LADP protocol." && sleep 0.1 && tmux send-keys -t $PANE3 Enter
```

## 9. Best Practices

### 9.1 Naming Conventions
- Always specify pane numbers explicitly
- Assign task IDs for trackability
- Include date/time and pane numbers in filenames

### 9.2 Error Handling
- Set timeouts for each task
- Automatic retry mechanisms on errors
- Prepare alternative plans in advance for failures

### 9.3 Performance Optimization
- Load balance heavy tasks
- Parallelize I/O-intensive tasks
- Execute CPU-intensive tasks sequentially

## 10. Common Problems and Solutions

### Q1: Pane Not Responding
```bash
# Force terminate and restart
tmux kill-pane -t $PANE1
tmux split-window -h
# Get new pane ID and reassign
```

### Q2: Out of Memory Error
```bash
# Clear all panes to free memory
for pane in $PANE1 $PANE2 $PANE3 $PANE4; do
    tmux send-keys -t $pane "/clear" && sleep 0.1 && tmux send-keys -t $pane Enter
done
```

### Q3: Synchronization Issues
```bash
# Implement barrier synchronization
echo "Waiting for all panes to complete..."
while true; do
    # Check status of each pane
    completed=0
    for pane in $PANE1 $PANE2 $PANE3 $PANE4; do
        if tmux capture-pane -t $pane -p | tail -1 | grep -q "completed"; then
            ((completed++))
        fi
    done
    
    if [ $completed -eq 4 ]; then
        echo "All panes completed!"
        break
    fi
    
    sleep 5
done
```

## 11. Security and Privacy

- Use `--dangerously-skip-permissions` flag only in development environments
- Process tasks containing sensitive information in a single pane
- Regular deletion of log files

---

Instructions from here

1. As your team, prepare 5 panes in tmux and start Claude Code instances in each pane.
2. First, you read LADP.md, and instruct the team to also read LADP.md to understand the protocol.
3. Proceed with the following in cooperation with each instance. Take meeting minutes while proceeding.

"Specific task here"

First, proceed while checking operation to ensure the sent prompt is confirmed with Enter and a response is returned from Claude.

3. After the discussion is complete, create a comprehensive report summarizing:
   - Key insights from each pane
   - Common themes and patterns identified
   - Synthesis of ideas across all perspectives
   - Practical applications and recommendations
   - Meta-insights about the collaborative process itself

4. Save the report as a separate file (e.g., `discussion_report.md`) and provide a concise summary of the main findings.
