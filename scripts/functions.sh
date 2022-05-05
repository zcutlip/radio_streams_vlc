# In shell, success is exit(0), error is anything else, e.g., exit(1)
SUCCESS=0
FAILURE=1

quit(){
    if [ $# -gt 1 ];
    then
        echo "$1"
        shift
    fi
    # shellcheck disable=SC2086
    exit $1
}

branch_is_master_or_main(){
    local branch
    branch=$(git rev-parse --abbrev-ref HEAD)
    if [ "$branch" = "master" ] || [ "$branch" = "main" ];
    then
        return $SUCCESS;
    else
        return $FAILURE;
    fi
}

branch_is_clean(){
    local modified
    modified=$(git ls-files -m) || quit "Unable to check for modified files." $?
    if [ -z "$modified" ];
    then
        return $SUCCESS;
    else
        return $FAILURE;
    fi
}

current_version() {
    local version
    version="$(python3 ./setup.py --version)" || quit "Unable to detect package version" $?
    printf "%s" "$version"
}

version_is_tagged(){
    local version="$1"
    # e.g., verion = 0.1.0
    # check if git tag -l v0.1.0 exists
    tag_description=$(git tag -l v"$version")
    if [ -n "$tag_description" ];
    then
        return $SUCCESS;
    else
        return $FAILURE;
    fi
}

prompt_yes_no(){
    if [ $# -gt 1 ];
    then
        prompt_string="$1"
    else
        prompt_string=""
    fi
    read -r -p "$prompt_string [Y/n] " response

    case $response in
    [yY][eE][sS]|[yY])
        return $SUCCESS
        ;;
        *)
        return $FAILURE
        ;;
    esac
}
