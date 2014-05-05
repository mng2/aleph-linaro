#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/time.h>
#include <limits.h>

#define MAP_SIZE 0x1000
#define REG_ID 0x0
#define REG_STATUS 0x1
#define REG_READ 0x2
#define REG_WRITE 0x3
#define REG_FULL 0x4

void usage(void)
{
    printf("usage: fifotest -d <UIO_DEV_FILE>\n");
}

int main(int argc, char *argv[])
{
    int c;
    int i;
    int fd = 0;
    char *uiod = 0;
    unsigned temp;

    volatile unsigned *uiomem;

    while ((c = getopt(argc, argv, "d:io:h")) != -1) {
        switch(c) {
        case 'd':
            uiod = optarg;
            break;
        case 'h':
            usage();
            return 0;
        default:
            printf("invalid option: %c\n", c);
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
    uiomem = (volatile unsigned *)mmap(NULL, MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
    if (!uiomem) {
        perror(argv[0]);
        printf("mmap error\n");
        return -1;
    }

    printf("UIO device: %s\n",uiod);
    printf("Module ID: 0x%08x\n",uiomem[REG_ID]);

    if (!(uiomem[REG_STATUS] == 0xfFFFfFFF))
    {
	i = 0;
        printf("FIFO not empty, emptying...\n");
        while (!(uiomem[REG_STATUS] == 0xfFFFfFFF))
        {
            uiomem[REG_READ] = 0x1;            // initiate read
            while (!((temp = uiomem[REG_READ]) & 0x10)) ; // wait for ack
            uiomem[REG_READ] = 0x0;           // signal read done
            while (uiomem[REG_READ] & 0x10) ; // wait for ack lowering
	    if ((0xFFFF & i) != (temp >> 16)) {
              printf("Error at 0x%04x: 0x%04x\n",i,(temp >> 16));
	    }
	    i++;
        }
    }

    printf("FIFO empty. %d values discarded.\n",i);
    printf("Writing values to FIFO...\n");


    for (i = 0; i < 100000; i++)
    {
       if (uiomem[REG_FULL] == 0xfFFFfFFF)
       {
           printf("Info: FIFO is full, %d values written\n",i);
	   printf("status 0x%08x\n",uiomem[REG_FULL]);
           break;
       }
        uiomem[REG_WRITE] = (i << 16) | 0x1;            // initiate write
        while (!((temp = uiomem[REG_WRITE]) & 0x10)) ; // wait for ack
        uiomem[REG_WRITE] = 0x0;           // signal write done
        while (uiomem[REG_WRITE] & 0x10) ; // wait for ack lowering
        //printf("wrote: 0x%04x\n",i);
    }

    printf("\n");

    munmap((void*)uiomem, MAP_SIZE);

    return 0;
}

