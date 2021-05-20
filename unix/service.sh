##########################################################################
# Restart all services, start, stop, and provide status about servers.  /+
##########################################################################

# run  sh service.sh  to see all the available options.

export service="${1%/*}"

sh ../astron/unix/start_pirates_services.sh
