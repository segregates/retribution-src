cd ..



usage () {
   echo 'Usage : sh service <service>'
    echo "                      Example: To start/restart all services."
    echo "                         sh service all"
    echo "                      Example: To start/restart astron."
    echo "                         sh service astron"
    echo "                      Example: To start/restart ai."
    echo "                         sh service ai"
    echo "                      Example: To start/restart uberdog."
    echo "                         sh service uberdog"
    echo "                      Example: To start/restart mongodb."
    echo "                         sh service mongo"
    echo "                      Example: To stop services."
    echo "                         sh service stop"
    echo "                      Example: To view if services are running."
    echo "                         sh service status"
    exit
}

if [ "$service" ]; then

    case "$service" in
        uberdog)
            sh astron/unix/uberdog.sh
            ;;
        ai)
           sh astron/unix/ai.sh
            ;;
        astron)
           sh astron/unix/astron.sh
            ;;
        mongo)
            sh astron/unix/mongo.sh
        ;;
        stop)
            pid[0]=$(pgrep -f "astron")
            pid[1]=$(pgrep -f "pirates.ai.ServiceStart")
            pid[2]=$(pgrep -f "pirates.uberdog.ServiceStart")

            for i in "${pid[@]}"
            do
                if [[ $i ]]; then
                    kill -9 $i
                fi
            done
        ;;
        status)

            astron_index=0;
            ai_index=1;
            uberdog_index=2;
            pid[$astron_index]=$(pgrep -f "astron/")
            pid[$ai_index]=$(pgrep -f "pirates.ai.ServiceStart")
            pid[$uberdog_index]=$(pgrep -f "pirates.uberdog.ServiceStart")

            if [ ${pid[$astron_index]} ]; then
                    echo "Aston is running PID# ${pid[$astron_index]}"
                else
                    echo "Aston is NOT running"
            fi

            if [ ${pid[$ai_index]} ]; then
                    echo "AI is running PID# ${pid[$ai_index]}"
                else
                    echo "AI is NOT running"
            fi

            if [ ${pid[$uberdog_index]} ]; then
                    echo "Uberdog is running PID# ${pid[$uberdog_index]}"
                else
                    echo "Uberdog is NOT running"
            fi

        ;;
        all)
            #sh astron/unix/mongo.sh
            sh astron/unix/astron.sh
            sh astron/unix/ai.sh
            sh astron/unix/uberdog.sh
            ;;
        *)
            echo " Service '"$service"'  was not found, a typo perhaps?\n"
            usage
            exit 1 #
      ;;
        esac

else
    usage
fi

