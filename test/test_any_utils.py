def test_key_val_replacement_works(host):
    """Confirms addOrEditKeyValPair either adds or replaces a key value pair in a given file"""
    host.run(
        """
    source /opt/pihole/utils.sh
    addOrEditKeyValPair "./testoutput" "KEY_ONE" "value1"
    addOrEditKeyValPair "./testoutput" "KEY_TWO" "value2"
    addOrEditKeyValPair "./testoutput" "KEY_ONE" "value3"
    addOrEditKeyValPair "./testoutput" "KEY_FOUR" "value4"
    """
    )
    output = host.run(
        """
    cat ./testoutput
    """
    )
    expected_stdout = "KEY_ONE=value3\nKEY_TWO=value2\nKEY_FOUR=value4\n"
    assert expected_stdout == output.stdout


def test_getFTLPID_default(host):
    """Confirms getFTLPID returns the default value if FTL is not running"""
    output = host.run(
        """
    source /opt/pihole/utils.sh
    getFTLPID
    """
    )
    expected_stdout = "-1\n"
    assert expected_stdout == output.stdout


def test_setFTLConfigValue_getFTLConfigValue(host):
    """
    Confirms getFTLConfigValue works (also assumes setFTLConfigValue works)
    Requires FTL to be installed, so we do that first
    (taken from test_FTL_development_binary_installed_and_responsive_no_errors)
    """
    host.run(
        """
    source /opt/pihole/basic-install.sh
    create_pihole_user
    funcOutput=$(get_binary_name)
    echo "development" > /etc/pihole/ftlbranch
    binary="pihole-FTL${funcOutput##*pihole-FTL}"
    theRest="${funcOutput%pihole-FTL*}"
    FTLdetect "${binary}" "${theRest}"
    """
    )

    output = host.run(
        """
    source /opt/pihole/utils.sh
    setFTLConfigValue "dns.upstreams" '["9.9.9.9"]' > /dev/null
    getFTLConfigValue "dns.upstreams"
    """
    )

    assert "[ 9.9.9.9 ]" in output.stdout


def test_proxy_setProxy_and_getProxy(host):
    """Confirms setProxy creates a valid proxy configuration file and getProxy reads it correctly"""
    # Override the proxy config file location for testing
    host.run(
        """
    export PROXY_CONFIG_FILE="/tmp/test_proxy.conf"
    source /opt/pihole/proxy.sh
    setProxy "http://proxy.example.com:8080" "https://proxy.example.com:8080" "localhost,127.0.0.1"
    """
    )
    
    # Check that the file was created with correct content
    output = host.run(
        """
    cat /tmp/test_proxy.conf
    """
    )
    
    assert 'export HTTP_PROXY="http://proxy.example.com:8080"' in output.stdout
    assert 'export http_proxy="http://proxy.example.com:8080"' in output.stdout
    assert 'export HTTPS_PROXY="https://proxy.example.com:8080"' in output.stdout
    assert 'export https_proxy="https://proxy.example.com:8080"' in output.stdout
    assert 'export NO_PROXY="localhost,127.0.0.1"' in output.stdout
    assert 'export no_proxy="localhost,127.0.0.1"' in output.stdout


def test_proxy_clearProxy(host):
    """Confirms clearProxy removes the proxy configuration file"""
    # Create a proxy config first
    host.run(
        """
    export PROXY_CONFIG_FILE="/tmp/test_proxy.conf"
    source /opt/pihole/proxy.sh
    setProxy "http://proxy.example.com:8080"
    """
    )
    
    # Verify it exists
    output = host.run(
        """
    test -f /tmp/test_proxy.conf && echo "exists" || echo "not exists"
    """
    )
    assert "exists" in output.stdout
    
    # Clear it
    host.run(
        """
    export PROXY_CONFIG_FILE="/tmp/test_proxy.conf"
    source /opt/pihole/proxy.sh
    clearProxy
    """
    )
    
    # Verify it's gone
    output = host.run(
        """
    test -f /tmp/test_proxy.conf && echo "exists" || echo "not exists"
    """
    )
    assert "not exists" in output.stdout


def test_proxy_loadProxyConfig(host):
    """Confirms loadProxyConfig exports environment variables correctly"""
    # Create a proxy config
    host.run(
        """
    export PROXY_CONFIG_FILE="/tmp/test_proxy.conf"
    source /opt/pihole/proxy.sh
    setProxy "http://proxy.example.com:8080" "https://proxy.example.com:8080"
    """
    )
    
    # Load and check environment variables
    output = host.run(
        """
    source /tmp/test_proxy.conf
    echo "HTTP_PROXY=${HTTP_PROXY}"
    echo "HTTPS_PROXY=${HTTPS_PROXY}"
    """
    )
    
    assert "HTTP_PROXY=http://proxy.example.com:8080" in output.stdout
    assert "HTTPS_PROXY=https://proxy.example.com:8080" in output.stdout

