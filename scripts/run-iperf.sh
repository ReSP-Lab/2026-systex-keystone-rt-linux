#!/bin/bash

PORT=5201
IP="192.168.1.207"

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
  -i)
      read -p "IP adress to connect to? " IP
      if [[ "$IP" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
        IFS='.' read -r i1 i2 i3 i4 <<< "$ip"
        if (( i1 <= 255 && i2 <= 255 && i3 <= 255 && i4 <= 255 )); then
            shift 1
        else
            echo "$IP is not a valid IP address."
            exit 1
        fi
      else
          echo "$IP is not a valid IP address."
          exit 1
      fi
      ;;
    -p)
      if [[ "$2" =~ ^[0-9]+$ ]]; then
        PORT="$2"
        shift 2
      else
        echo "Error: -p requires a numeric PORT value"
        exit 1
      fi
      ;;
    -a)
      if [[ -n "$2" ]]; then
        IP="$2"
        shift 2
      else
        echo "Error: -a requires a ip adress"
        exit 1
      fi
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

iperf3 -c $IP -p $PORT -w 64k -P 100 -t 5800