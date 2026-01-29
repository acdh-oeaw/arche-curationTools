#/bin/bash
if [ "$1" == "" ] ; then
    echo "Usage: $0 namespace"
    exit
fi
pod="$1"
if [ "$2" != "" ] ; then
    pod="$2"
fi
pod=`kubectl get pods --namespace "$1" --kubeconfig=acdh-ch-cluster-2.yaml | grep Running | grep "$pod" | head -n 1 | sed -e 's/ .*//'`
if [ "$pod" == "" ] ; then
    exit "No pods found"
fi
echo "kubectl exec --kubeconfig=acdh-ch-cluster-2.yaml --stdin --tty --namespace \"$1\" \"$pod\" -- /bin/bash"
winpty > /dev/null 2>&1
if [ "$?" == "127" ] ; then
    kubectl exec --kubeconfig=acdh-ch-cluster-2.yaml --stdin --tty --namespace "$1" "$pod" -- bash
else
    winpty kubectl exec --kubeconfig=acdh-ch-cluster-2.yaml --stdin --tty --namespace "$1" "$pod" -- bash
fi

