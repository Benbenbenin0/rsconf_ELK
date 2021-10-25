#!/bin/bash
postfix_rsconf_component() {
rsconf_yum_install postfix procmail cyrus-sasl cyrus-sasl-plain
rsconf_service_prepare 'postfix' '/etc/systemd/system/postfix.service' '/etc/systemd/system/postfix.service.d' '/etc/postfix'
rsconf_install_access '440' 'root' 'mail'
rsconf_install_file '/etc/postfix/sender_access' '0b4502ada3610b0add93020a51164241'
rsconf_install_access '400' 'root' 'root'
rsconf_install_file '/etc/postfix/v9.radia.run.key' '79217e58aceeddf749b58dac0c9c2c84'
rsconf_install_file '/etc/postfix/v9.radia.run.crt' 'a2fa2f430397fa91705e4e07ce23e60b'
rsconf_install_access '644' 'root' 'root'
rsconf_install_file '/etc/postfix/main.cf' 'e16fe8ac2764b168cee4bcf28c142a7f'
rsconf_install_file '/etc/postfix/master.cf' '7963eb585d2f004631f7a78748d4dac7'
rsconf_install_file '/etc/aliases' '505977dfd514ab835c60dacf40535cd1'
postfix_main
rsconf_service_restart_at_end 'postfix'
}
#!/bin/bash

postfix_main() {
    # never hurts
    newaliases
}



# Testing email
true <<'EOF2'
/usr/sbin/sendmail fourem@petshop.v4.radia.run <<'EOF'
To: fourem@petshop.v4.radia.run
Subject: testing 123
From: vagrant+btest_btest_admin@v4.radia.run

test
EOF
EOF2

