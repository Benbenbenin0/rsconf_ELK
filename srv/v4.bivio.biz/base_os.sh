#!/bin/bash

base_os_chrony() {
    if [[ ! -f /vagrant/Vagrantfile ]]; then
        # only needed for vagrant
        return
    fi
    local x=/etc/systemd/system/rsconf-chrony-makestep.service
    if [[ -r $x ]]; then
        return
    fi
cat > "$x" <<'EOF'
[Unit]
Description=Force chrony to synchronize (makestep) system clock
After=chronyd.service
Requires=chronyd.service
Before=time-sync.target
Wants=time-sync.target

[Service]
Type=oneshot
ExecStart=/usr/bin/chronyc -a makestep
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
    systemctl enable rsconf-chrony-makestep
    systemctl start rsconf-chrony-makestep
}

base_os_main() {
    local i=$(sysctl -n net.ipv6.conf.all.disable_ipv6)
    local reboot=
    rsconf_install_access 400 root root
    rsconf_install_file /etc/sysctl.d/60-rsconf-base.conf
#TODO(robnagler) return result to test install?
    sysctl -p --system
    if (( $i == 0 )); then
        reboot=1
        # https://access.redhat.com/solutions/8709
        # Must be done first time
        install_info 'Rebuilding initrd to disable ipv6'
        # Not bothering with backup, because this only happens once after fresh
        # restart.
        dracut -f
    fi
    if [[ ! -e /etc/yum.repos.d/epel.repo ]]; then
        yum --enablerepo=extras install -y -q epel-release
    fi
    local x=(
#TODO(robnagler) hardwire versions
#TODO(robnagler) local check of rpm so don't hit slow net unless necessary
        bind-utils # rsconf (dig)
        emacs-nox
        git # rsconf (dig)
        lsof # debugging
        patch # python/pyenv
        perl # general and git
        readline-devel # python/pyenv
        sqlite-devel # python/pyenv
        strace # debugging
        unzip # rsconf
        wget # many tools
    )

    rsconf_yum_install "${x[@]}"
    # https://access.redhat.com/solutions/8709
    # breaks SSH Xforwarding unless AddressFamily inet is set in sshd_config
    # idempotent so ok to repeat and the file might get updated with a new release.
    rsconf_edit /etc/ssh/sshd_config ^AddressFamily.inet \
        's{^#(AddressFamily) any}{$1 inet}' || true
    # Binding to IPv6 address not available since kernel does not support IPv6.
    # https://bugzilla.redhat.com/show_bug.cgi?id=1402961
    if rsconf_edit /usr/lib/systemd/system/rpcbind.socket '! BindIPv6Only' \
        'm{\[::\]:|BindIPv6Only} && ($_ = q{})'; then
        systemctl daemon-reload
        systemctl restart rpcbind.socket
    fi
#TODO(robnagler) consider permissive on back end and enforcing on front end
    if rsconf_edit /etc/selinux/config ^SELINUX=disabled \
        's{(?<=^SELINUX=).*}{disabled}'; then
        reboot=1
    fi
    base_os_chrony
    if [[ -n $reboot ]]; then
        rsconf_reboot
    fi
}
