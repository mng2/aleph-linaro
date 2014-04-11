#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/time.h>
#include <limits.h>

#define MAP_SIZE 0x1000

char *strdup(const char *);

void usage(void)
{
    printf("usage: uiopoke -d <UIO_DEV_FILE> -a <address> [-w <word>]\n");
}

int main(int argc, char *argv[])
{
    int fd = 0;
    char *uiod, *addr, *value; 
    int Write = 0;
    unsigned temp, address;

    volatile unsigned *uioreg;

    int option = -1;
    while ((option = getopt(argc, argv, "d:a:w:h:")) != -1)
    {
        switch(option)
        {
        case 'd':
            uiod = strdup(optarg);
            break;
	case 'a':
 	    addr = strdup(optarg);
 	    break;
	case 'w':
	    Write = 1;
	    value = strdup(optarg);
	    break;
        case 'h':
            usage();
            return 0;
        default:
            printf("invalid option: %c\n", (char)option);
            usage();
            return -1;
        }
    }

    if (!uiod) {
        usage();
        return -1;
    }

    /* Open the UIO device file */
    fd = open(uiod, O_RDWR);
    if (fd < 1) {
        perror(argv[0]);
        printf("Invalid UIO device file: '%s'\n", uiod);
        return -1;
    }

    /* mmap the UIO device */
    uioreg = (volatile unsigned *)mmap(NULL, MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
    if (!uioreg) {
        perror(argv[0]);
        printf("mmap\n");
        return -1;
    }

    address = atoi(addr);

    if (Write) {
	uioreg[address]= atoi(value);
    }

    temp = uioreg[address];
    printf("read %u: %8x\n ",address,temp);

    munmap((void*)uioreg, MAP_SIZE);
    return 0;
}

