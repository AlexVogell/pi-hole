#!/usr/bin/env bash

# Pi-hole: A black hole for Internet advertisements
# (c) 2017 Pi-hole, LLC (https://pi-hole.net)
# Network-wide ad blocking via your own hardware.
#
# Script to manage proxy configuration for Pi-hole
#
# This file is copyright under the latest version of the EUPL.
# Please see LICENSE file for your rights under this license.

: "${PI_HOLE_SCRIPT_DIR:=/opt/pihole}"
: "${PROXY_CONFIG_FILE:=/etc/pihole/proxy.conf}"

# shellcheck source=./COL_TABLE
if [[ -f "${PI_HOLE_SCRIPT_DIR}/COL_TABLE" ]]; then
    source "${PI_HOLE_SCRIPT_DIR}/COL_TABLE"
else
    # Define minimal color variables if COL_TABLE is not available
    TICK="[✓]"
    CROSS="[✗]"
    INFO="[i]"
    COL_NC=""
    COL_GREEN=""
    COL_RED=""
fi

#######################
# Set proxy configuration
#
# Takes up to three arguments: http_proxy, https_proxy, no_proxy
# Example: setProxy "http://proxy.example.com:8080" "https://proxy.example.com:8080" "localhost,127.0.0.1"
#######################
setProxy() {
    local http_proxy="${1}"
    local https_proxy="${2}"
    local no_proxy="${3}"
    
    # Create or clear the proxy config file
    : > "${PROXY_CONFIG_FILE}"
    
    # Add proxy settings if provided
    if [[ -n "${http_proxy}" ]]; then
        echo "export HTTP_PROXY=\"${http_proxy}\"" >> "${PROXY_CONFIG_FILE}"
        echo "export http_proxy=\"${http_proxy}\"" >> "${PROXY_CONFIG_FILE}"
    fi
    
    if [[ -n "${https_proxy}" ]]; then
        echo "export HTTPS_PROXY=\"${https_proxy}\"" >> "${PROXY_CONFIG_FILE}"
        echo "export https_proxy=\"${https_proxy}\"" >> "${PROXY_CONFIG_FILE}"
    fi
    
    if [[ -n "${no_proxy}" ]]; then
        echo "export NO_PROXY=\"${no_proxy}\"" >> "${PROXY_CONFIG_FILE}"
        echo "export no_proxy=\"${no_proxy}\"" >> "${PROXY_CONFIG_FILE}"
    fi
    
    # Set proper permissions
    chmod 644 "${PROXY_CONFIG_FILE}"
    
    echo -e "  ${TICK} Proxy configuration saved"
}

#######################
# Clear proxy configuration
#######################
clearProxy() {
    if [[ -f "${PROXY_CONFIG_FILE}" ]]; then
        rm -f "${PROXY_CONFIG_FILE}"
        echo -e "  ${TICK} Proxy configuration cleared"
    else
        echo -e "  ${INFO} No proxy configuration to clear"
    fi
}

#######################
# Display proxy configuration
#######################
getProxy() {
    if [[ -f "${PROXY_CONFIG_FILE}" ]]; then
        echo -e "  ${INFO} Current proxy configuration:"
        # shellcheck source=/dev/null
        source "${PROXY_CONFIG_FILE}"
        
        [[ -n "${HTTP_PROXY}" ]] && echo "  HTTP Proxy:  ${HTTP_PROXY}"
        [[ -n "${HTTPS_PROXY}" ]] && echo "  HTTPS Proxy: ${HTTPS_PROXY}"
        [[ -n "${NO_PROXY}" ]] && echo "  No Proxy:    ${NO_PROXY}"
    else
        echo -e "  ${INFO} No proxy configured"
    fi
}

#######################
# Load proxy configuration for use in scripts
# This function should be sourced by scripts that need proxy support
#######################
loadProxyConfig() {
    if [[ -f "${PROXY_CONFIG_FILE}" ]]; then
        # shellcheck source=/dev/null
        source "${PROXY_CONFIG_FILE}"
    fi
}
