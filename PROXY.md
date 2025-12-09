# Proxy Configuration for Pi-hole

Pi-hole now supports optional proxy configuration for all network operations, including:
- Downloading blocklists (gravity updates)
- Checking for Pi-hole updates
- Uploading debug logs
- Downloading FTL binary during installation

This is particularly useful for users behind corporate proxies or those who want to route Pi-hole's traffic through a proxy server.

## Features

- Support for HTTP, HTTPS, and SOCKS5 proxies
- Ability to exclude specific hosts from proxying (NO_PROXY)
- Simple CLI commands for managing proxy settings
- Automatic proxy usage by all Pi-hole network operations
- No configuration required - works out of the box without a proxy

## Usage

### Setting a Proxy

To configure Pi-hole to use a proxy, use the `setproxy` command:

```bash
# Set HTTP and HTTPS proxy
sudo pihole setproxy http://proxy.example.com:8080 https://proxy.example.com:8080

# Set only HTTP proxy
sudo pihole setproxy http://proxy.example.com:8080

# Set proxy with exclusions
sudo pihole setproxy http://proxy.example.com:8080 https://proxy.example.com:8080 "localhost,127.0.0.1,.local"

# Set SOCKS5 proxy
sudo pihole setproxy socks5://proxy.example.com:1080
```

### Viewing Current Proxy Configuration

To view the current proxy configuration:

```bash
pihole getproxy
```

This will display the configured HTTP proxy, HTTPS proxy, and any exclusions.

### Clearing Proxy Configuration

To remove the proxy configuration:

```bash
sudo pihole clearproxy
```

### Help

To get help on proxy commands:

```bash
pihole setproxy --help
```

## Configuration File

Proxy settings are stored in `/etc/pihole/proxy.conf` as environment variables. This file is automatically sourced by Pi-hole scripts that perform network operations.

The file contains standard proxy environment variables:
- `HTTP_PROXY` / `http_proxy` - Proxy for HTTP requests
- `HTTPS_PROXY` / `https_proxy` - Proxy for HTTPS requests
- `NO_PROXY` / `no_proxy` - Comma-separated list of hosts to exclude from proxying

## Proxy URL Format

Proxy URLs should follow this format:

- HTTP proxy: `http://hostname:port`
- HTTPS proxy: `https://hostname:port`
- SOCKS5 proxy: `socks5://hostname:port`
- With authentication: `http://username:password@hostname:port`

## Examples

### Corporate Proxy

```bash
sudo pihole setproxy http://proxy.corp.example.com:8080 https://proxy.corp.example.com:8080 "localhost,127.0.0.1,.local,.corp.example.com"
```

### SOCKS5 Proxy (e.g., SSH tunnel)

```bash
sudo pihole setproxy socks5://localhost:1080
```

### Authenticated Proxy

```bash
sudo pihole setproxy "http://user:pass@proxy.example.com:8080"
```

## Testing Proxy Configuration

After configuring a proxy, test it by updating gravity:

```bash
sudo pihole -g
```

You should see Pi-hole download blocklists through your configured proxy.

## Troubleshooting

### Proxy not working

1. Verify your proxy configuration:
   ```bash
   pihole getproxy
   ```

2. Check if the proxy is accessible:
   ```bash
   curl -x http://proxy.example.com:8080 https://api.github.com/
   ```

3. Check Pi-hole logs for connection errors:
   ```bash
   tail -f /var/log/pihole/pihole.log
   ```

### Clearing proxy after network change

If you change networks and no longer need a proxy:

```bash
sudo pihole clearproxy
```

## Technical Details

### How It Works

1. Proxy settings are stored in `/etc/pihole/proxy.conf`
2. This file is automatically sourced by:
   - `gravity.sh` - for blocklist downloads
   - `piholeDebug.sh` - for debug log uploads
   - `updatecheck.sh` - for update checks
   - `basic-install.sh` - for FTL binary downloads
3. The `curl` command automatically respects the standard `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables

### Environment Variable Precedence

If you have proxy environment variables set in your shell, they will be overridden by Pi-hole's proxy configuration. To use system-wide proxy settings instead, don't configure Pi-hole's proxy.

## Notes

- Proxy settings require root/sudo privileges to modify
- Proxy settings are persistent across reboots
- The proxy is only used for Pi-hole's own network operations, not for DNS queries
- Authenticated proxies are supported but credentials are stored in plain text in `/etc/pihole/proxy.conf`
