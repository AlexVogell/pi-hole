# Pi-hole Proxy Configuration

Pi-hole now supports optional proxy configuration for all network operations, including downloading blocklists, updating Pi-hole components, and accessing external resources.

## Overview

Users who need to route Pi-hole's network traffic through a proxy (HTTP, HTTPS, or SOCKS5) can now configure this directly through the Pi-hole CLI. This is particularly useful for:

- Users behind corporate firewalls
- Those using privacy-focused SOCKS proxies (like Mullvad, Tor, etc.)
- Network setups that require all traffic to go through a proxy server
- Users who frequently switch between different network configurations

## Configuration

### Using the CLI

The `pihole proxy` command provides a simple interface to manage proxy settings:

#### Set a Proxy

```bash
# Set HTTP proxy
sudo pihole proxy set http http://proxy.example.com:8080

# Set HTTPS proxy
sudo pihole proxy set https https://secure-proxy.example.com:8443

# Set SOCKS5 proxy for all protocols
sudo pihole proxy set all socks5://127.0.0.1:1080

# Set proxy with authentication
sudo pihole proxy set http http://username:password@proxy.example.com:8080
```

#### View Current Settings

```bash
sudo pihole proxy show
```

This will display:
```
Current proxy settings:
  HTTP proxy:  http://proxy.example.com:8080
  HTTPS proxy: https://secure-proxy.example.com:8443
  All proxy:   (not set)
```

#### Clear Proxy Settings

```bash
# Clear HTTP proxy only
sudo pihole proxy clear http

# Clear HTTPS proxy only
sudo pihole proxy clear https

# Clear all proxy settings
sudo pihole proxy clear all
```

#### Get Help

```bash
sudo pihole proxy --help
```

### Direct Configuration

Proxy settings are stored in Pi-hole's FTL configuration. You can also configure them directly using:

```bash
# Set HTTP proxy
sudo pihole-FTL --config misc.http_proxy "http://proxy.example.com:8080"

# Set HTTPS proxy
sudo pihole-FTL --config misc.https_proxy "https://secure-proxy.example.com:8443"

# Set all-protocol proxy (SOCKS5)
sudo pihole-FTL --config misc.all_proxy "socks5://127.0.0.1:1080"
```

## Supported Proxy Types

Pi-hole supports the following proxy protocols through curl:

- **HTTP proxies**: `http://proxy.example.com:8080`
- **HTTPS proxies**: `https://proxy.example.com:8443`
- **SOCKS4 proxies**: `socks4://proxy.example.com:1080`
- **SOCKS4a proxies**: `socks4a://proxy.example.com:1080`
- **SOCKS5 proxies**: `socks5://proxy.example.com:1080`
- **SOCKS5h proxies** (with remote DNS resolution): `socks5h://proxy.example.com:1080`

### Authentication

Proxies that require authentication can be configured with credentials in the URL:

```bash
sudo pihole proxy set http http://username:password@proxy.example.com:8080
```

**Security Note**: Be cautious when including passwords in proxy URLs as they will be stored in Pi-hole's configuration.

## How It Works

Once configured, Pi-hole automatically uses the proxy settings for:

1. **Gravity updates** (`pihole -g`): When downloading blocklists
2. **Pi-hole updates** (`pihole -up`): When updating Pi-hole components
3. **FTL binary downloads**: When installing or updating FTL
4. **Other network operations**: Any operation that uses curl or respects standard proxy environment variables

The proxy configuration is loaded by:
- `gravity.sh` - for blocklist downloads
- `update.sh` - for Pi-hole updates
- Other scripts that source `utils.sh` and call `loadProxyConfiguration`

## Environment Variables

When proxy settings are configured, Pi-hole exports the following environment variables:

- `HTTP_PROXY` / `http_proxy`
- `HTTPS_PROXY` / `https_proxy`
- `ALL_PROXY` / `all_proxy`

These are standard environment variables recognized by curl, wget, and many other networking tools.

## Troubleshooting

### Verify Proxy Settings

```bash
sudo pihole proxy show
```

### Test Proxy Connection

After configuring a proxy, test it by running a gravity update:

```bash
sudo pihole -g
```

Check the output for any connection errors.

### Check Environment Variables

To verify that proxy environment variables are being set correctly:

```bash
sudo bash -c 'source /opt/pihole/utils.sh && loadProxyConfiguration && env | grep -i proxy'
```

### Clear Proxy Settings

If you encounter issues, clear all proxy settings:

```bash
sudo pihole proxy clear all
```

### Proxy Authentication Issues

If your proxy requires authentication and you're experiencing issues:

1. Ensure credentials are properly URL-encoded
2. Check that your proxy server accepts the authentication method
3. Try setting the proxy without credentials first to isolate the issue

## Examples

### Corporate Proxy Setup

```bash
# Configure HTTP and HTTPS proxies for corporate network
sudo pihole proxy set http http://proxy.corp.example.com:8080
sudo pihole proxy set https http://proxy.corp.example.com:8080

# Verify settings
sudo pihole proxy show

# Update gravity to test
sudo pihole -g
```

### SOCKS5 Proxy (e.g., Mullvad, Tor)

```bash
# Configure SOCKS5 proxy for all traffic
sudo pihole proxy set all socks5://127.0.0.1:1080

# Verify settings
sudo pihole proxy show

# Update gravity to test
sudo pihole -g
```

### Switching Networks

When moving between networks with different proxy requirements:

```bash
# At work - use corporate proxy
sudo pihole proxy set all http://proxy.corp.example.com:8080

# At home - clear proxy
sudo pihole proxy clear all
```

## See Also

- [Pi-hole Documentation](https://docs.pi-hole.net/)
- [curl Proxy Documentation](https://curl.se/docs/manpage.html#-x)
- [Standard Proxy Environment Variables](https://about.gitlab.com/blog/2021/01/27/we-need-to-talk-no-proxy/)
