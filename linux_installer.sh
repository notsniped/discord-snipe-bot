#!/bin/bash
function try()
{
    [[ $- = *e* ]]; SAVED_OPT_E=$?
    set +e
}

function throw()
{
    exit $1
}

function catch()
{
    export exception_code=$?
    (( $SAVED_OPT_E )) && set +e
    return $exception_code
}
echo "- Installing dependency modules..."
try
(
    pip install discord > /dev/null
    echo "- Installed discord!"
    echo "- Complete! (Installed 1 dependency library: discord)"
)
catch || {
   case $exc_code in
        *)
            echo "! Error installing modules"
            throw $exc_code
        ;;
    esac
}
