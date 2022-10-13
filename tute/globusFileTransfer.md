#GLOBUS file transfer protocol tutorial
Oct. 12, 2022
Orgho Neogi<anoronyo@gmail.com>

## Introduction

Globus is a service that provides tools for data management, including file transfer.
Globus transfers files using GridFTP.
GridFTP is a high-performance data transfer protocol, which is optimized for high-bandwidth, wide-area networks.
Globus provides more optimized file transfer and synchronization than scp or rsync.
It is asynchronous and works on a fire and forget model, resubmitting requests as necessary and providing notifications of tasks in progress and completed via email.

For more information regarding globus, you can visit their [homepage](https://www.globus.org/).

## Globus Account and Login

Both SLAC and fermilab have institutional accounts with globus and as such you can login to globus with either of them.
Any other accounts that can be found on their institutional list can also be used as can a google account.

Detailed list of instructions on how to logon to globus can be found [here.](https://docs.globus.org/how-to/get-started/)

## Globus-Cli

For the purposes of this tutorial, I will be giving instructions for the command line utility that globus exposes.
They also have a web interface and if you wish to use that, here are the [instructions.](https://www.globus.org/get-started)

I am favoring the Cli because it allows the submition of batch jobs.

[Here are the instructions for installing the cli on your local machine.](https://docs.globus.org/cli/)

## Setting up environmental variables

Because the cli relies on long id numbers to communicate with any endpoints, it can be worth it to put those id's in environment variables. If you use this often, it may be worth adding the following lines to your .

``` bash
export sdf_ep="dda770be-f428-11eb-ab64-d195c983855c"
export wc_ep="b251fb72-0f23-11eb-abe1-0213fe609573"
```

More generalized environmental variables to be setup can be found [here](https://docs.globus.org/cli/environment_variables/)
These variables are for interacting with the globus SDK.

## Endpoint activation

The first thing to do would be to login to the globus cli. You c an run the following command to do so.

``` bash
globus login
```

This will only seamlesly work if the cli can open up a browser window. If you're ssh'ed into a machine, the login instructions can be found [here](https://docs.globus.org/cli/quickstart/)

To confirm that you're logged into globus, you can run

``` bash
 globus get-identities -v 'go@globusid.org'
```

If you are not authenticated, you will see a message similar to: `Globus CLI Error: No Authentication provided.`

The first time these endpoints are used, they may not be activated. In order to activate them, run the following commands

``` bash
#Activating the SLAC sdf endpoint
globus endpoint activate --web $sdf_ep
#Activating the wc endpoint
globus endpoint activate --web $wc_ep
```

## Transferring files

Single files and directories can be recursively copied interactively without needing to invoke batch mode. A transfer can be done with the following syntax

``` bash
#Generic syntax
globus transfer <source_endpoint>:<filePath> <destination_endpoint>:<filePath>
#From wc to sdf
globus transfer $wc_ep:<filepath> $sdf_ep:<filepath>
#from sdf to wc
globus transfer $sdf_ep:<filepath> $wc_ep:<filepath>
```

More detailed guide can be found [here](https://docs.globus.org/cli/reference/transfer/)

A list of frequently asked questions for the globus service can be found [here](https://docs.globus.org/faq/globus-connect-endpoints/)
