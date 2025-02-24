#!/bin/bash
petshop_rsconf_component() {
rsconf_service_prepare 'petshop' '/etc/systemd/system/petshop.service' '/etc/systemd/system/petshop.service.d' '/srv/petshop' 'bivio-perl-dev.rpm' 'perl-Bivio-dev.rpm'
rsconf_install_access '711' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/petshop'
rsconf_install_access '755' 'vagrant' 'vagrant'
rsconf_install_access '500' 'vagrant' 'vagrant'
rsconf_install_file '/srv/petshop/reload' '2449c2da2eca4f9e6db48d224b6c53f1'
rsconf_install_file '/srv/petshop/start' 'fd195f649af0277ccb707a4e8f66b758'
rsconf_install_file '/srv/petshop/stop' 'ab019e77fc31e5dbf7fd06f0d42d58f8'
rsconf_install_access '444' 'root' 'root'
rsconf_install_file '/etc/systemd/system/petshop.service' '9fd1c96fb1f1f0ad0d8330da7e2d2a65'
rsconf_install_access '700' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/petshop/bkp'
rsconf_install_directory '/srv/petshop/db'
rsconf_install_directory '/srv/petshop/log'
rsconf_install_directory '/srv/petshop/logbop'
rsconf_install_access '711' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/petshop/srv'
rsconf_install_access '440' 'vagrant' 'vagrant'
rsconf_install_file '/srv/petshop/httpd.conf' '57ce9ecbcf54d2c54c2f36fec52e09f8'
rsconf_install_file '/srv/petshop/bivio.bconf' '936a8105c290cefc6aa4930b72273f2a'
rsconf_install_file '/srv/petshop/initdb.sh' '327fb6a8b971b9abb4b769db0d1fd940'
rsconf_install_symlink '../../../etc/httpd/modules' '/srv/petshop/modules'
rsconf_install_access '400' 'root' 'root'
rsconf_install_file '/etc/logrotate.d/petshop' '2ab0da60801c194a56dbc76b265263c3'
source /srv/petshop/initdb.sh
rsconf_install_access '711' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/petshop/srv/petshop'
rsconf_install_directory '/srv/petshop/srv/petshop/m'
rsconf_install_access '444' 'vagrant' 'vagrant'
rsconf_install_file '/srv/petshop/srv/petshop/m/maintenance.html' '14e798942cbbe2d8531db1cf10a737f6'
rsconf_install_file '/etc/nginx/conf.d/star.v4.radia.run.key' '031805b0a7c2e0fd1330b0613f385ede'
rsconf_install_file '/etc/nginx/conf.d/star.v4.radia.run.crt' '19cdea6247d259c6ffb2b36726ea297c'
rsconf_install_access '400' 'root' 'root'
rsconf_install_file '/etc/nginx/conf.d/petshop.v4.radia.run.conf' '1f9c2e06f665252fbc0fda68eab2ee22'
rsconf_install_access '711' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/petshop/srv/beforeother'
rsconf_install_directory '/srv/petshop/srv/beforeother/m'
rsconf_install_access '444' 'vagrant' 'vagrant'
rsconf_install_file '/srv/petshop/srv/beforeother/m/maintenance.html' '14e798942cbbe2d8531db1cf10a737f6'
rsconf_install_access '400' 'root' 'root'
rsconf_install_file '/etc/nginx/conf.d/beforeother.v4.radia.run.conf' 'adf8e98a495778f9a250ebee53986dbe'
rsconf_install_access '711' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/petshop/srv/m-petshop'
rsconf_install_directory '/srv/petshop/srv/m-petshop/m'
rsconf_install_access '444' 'vagrant' 'vagrant'
rsconf_install_file '/srv/petshop/srv/m-petshop/m/maintenance.html' '14e798942cbbe2d8531db1cf10a737f6'
rsconf_install_access '400' 'root' 'root'
rsconf_install_file '/etc/nginx/conf.d/m-petshop.v4.radia.run.conf' '4827e8b604104474ed0c0f761e024384'
rsconf_install_access '711' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/petshop/srv/other'
rsconf_install_directory '/srv/petshop/srv/other/m'
rsconf_install_access '444' 'vagrant' 'vagrant'
rsconf_install_file '/srv/petshop/srv/other/m/maintenance.html' '14e798942cbbe2d8531db1cf10a737f6'
rsconf_install_access '400' 'root' 'root'
rsconf_install_file '/etc/nginx/conf.d/other.v4.radia.run.conf' '97a0fa6dc62a4ca1d3031d28edf3d7c8'
rsconf_install_access '711' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/petshop/srv/requiresecure'
rsconf_install_directory '/srv/petshop/srv/requiresecure/m'
rsconf_install_access '444' 'vagrant' 'vagrant'
rsconf_install_file '/srv/petshop/srv/requiresecure/m/maintenance.html' '14e798942cbbe2d8531db1cf10a737f6'
rsconf_install_access '400' 'root' 'root'
rsconf_install_file '/etc/nginx/conf.d/requiresecure.v4.radia.run.conf' '5c3b7f79a997393bbfd705bb94fcee8a'
rsconf_install_access '400' 'vagrant' 'vagrant'
rsconf_install_file '/srv/petshop/db_bkp.sh' '076cdaeac7e0802fcbd388ad8f2434f3'
rsconf_install_access '700' 'vagrant' 'vagrant'
rsconf_install_directory '/srv/petshop/db_bkp'
}
