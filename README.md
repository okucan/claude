# SSH Remote Connection

Tools for connecting to the remote Ubuntu server.

## Quick Connect

```bash
ssh -i "myopenclaw.pem" ubuntu@23.23.211.5
```

## Using the connect script

```bash
chmod +x connect.sh

# Interactive shell
./connect.sh

# Run a command
./connect.sh 'uptime'

# Custom key/host
./connect.sh -i /path/to/key.pem -h 23.23.211.5
```

## Using ssh_config

```bash
# Add to ~/.ssh/config then connect with:
ssh server

# Or use the local config directly:
ssh -F ssh_config server
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SSH_KEY_FILE` | `myopenclaw.pem` | Path to PEM key file |
| `REMOTE_USER` | `ubuntu` | Remote username |
| `REMOTE_HOST` | `23.23.211.5` | Remote host/IP |

## Key File Setup

Ensure your PEM key has the correct permissions:

```bash
chmod 600 myopenclaw.pem
```
