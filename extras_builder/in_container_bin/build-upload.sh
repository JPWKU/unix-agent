#!/bin/bash

if [ -z $DCM_AWS_EXTRAS_BUCKET ]; then
    echo "DCM_AWS_EXTRAS_BUCKET env must be set"
    exit 1
fi
if [ -z $DCM_AGENT_EXTRAS_VERSION ]; then
    echo "You must set the version to build with the env DCM_AGENT_EXTRAS_VERSION"
    exit 1
fi

distro_all=`/bin/distro.sh`
echo $distro_all
distro=`echo $distro_all | awk '{ print $1 }'`
pkg_ext=`echo $distro_all | awk '{ print $2 }'`

echo $distro

git config --global user.email "packager@myco" && git config --global user.name "Omnibus Packager"
curl -s -L https://www.opscode.com/chef/install.sh | bash

export PATH=/opt/chef/embedded/bin:${PATH}
cd /omnibus-dcm-agent-extras
bundle install --binstubs
bin/omnibus build dcm-agent-extras
pkg=`ls -tC1 /omnibus-dcm-agent-extras/pkg/ | grep -v json | head -n 1`
new_pkg=dcm-agent-extras-$distro-$DCM_AGENT_EXTRAS_VERSION.$pkg_ext

if [ -z $AWS_ACCESS_KEY ]; then
    echo "AWS_ACCESS_KEY is not set"
    exit 1
fi
if [ -z $AWS_SECRET_KEY ]; then
    echo "AWS_SECRET_KEY is not set"
    exit 1
fi

s3cmd info s3://$DCM_AWS_EXTRAS_BUCKET/$new_pkg
if [ $? -eq 0 ]; then
    echo "The extras package already exists..."
    if [ -z $DCM_EXTRAS_FORCE_REBUILD ]; then
        echo "Quiting the build early"
        exit 0
    fi
fi

sed -i -e s^AWS_ACCESS_KEY^$AWS_ACCESS_KEY^ -e s^AWS_SECRET_KEY^$AWS_SECRET_KEY^ /root/.s3cfg

echo "Sending $pkg to $new_pkg"
s3cmd mb s3://$DCM_AWS_EXTRAS_BUCKET
s3cmd --progress --acl-public put /omnibus-dcm-agent-extras/pkg/$pkg s3://$DCM_AWS_EXTRAS_BUCKET/$new_pkg
