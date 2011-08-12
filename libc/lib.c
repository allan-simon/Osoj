#include <stdio.h>
#include <unistd.h>
#include <errno.h>

pid_t fork()
{
    errno = EPERM;
    return (pid_t)-1;
}
