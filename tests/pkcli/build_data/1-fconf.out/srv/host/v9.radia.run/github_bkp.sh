#!/bin/bash
github_bkp_rsconf_component() {
rsconf_service_prepare 'github_bkp.timer' '/etc/systemd/system/github_bkp.service' '/etc/systemd/system/github_bkp.timer' '/srv/github_bkp'
rsconf_install_access '700' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/github_bkp'
rsconf_install_access '500' 'vagrant' 'vagrant'
rsconf_install_file '/srv/github_bkp/cmd' 'c0e7e95966e57c57970066184419e6e6'
rsconf_install_file '/srv/github_bkp/env' '3985dcda6ffe393051c35405cb654b73'
rsconf_install_file '/srv/github_bkp/remove' '0c8f408a56cebd4e164b92e774c2e0e1'
rsconf_install_file '/srv/github_bkp/start' 'ddeedac7f12710020f86e0e15a455795'
rsconf_install_file '/srv/github_bkp/stop' '55477c8b1c0bf2d9f49829306d9b3759'
rsconf_install_access '444' 'root' 'root'
rsconf_install_file '/etc/systemd/system/github_bkp.timer' 'bca46813a5c7dd3020c622bb92712662'
rsconf_install_file '/etc/systemd/system/github_bkp.service' 'c4c23cec8aeb4c20d03f4a2497e5bcaf'
rsconf_service_docker_pull 'docker.io/radiasoft/beamsim:dev' 'github_bkp'
rsconf_install_access '500' 'vagrant' 'vagrant'
rsconf_install_file '/srv/github_bkp/run' '27969640e856d5bed8c1fd73d29afad2'
rsconf_install_access '700' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/github_bkp/db'
}
