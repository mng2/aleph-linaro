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

void usage(void)
{
    printf("usage: readadc -d <UIO_DEV_FILE>\n");
}

int main(int argc, char *argv[])
{
    int i;
    unsigned tempL, tempR;

    /* Open the UIO device files */
    int fd_adcL = 0;
    volatile unsigned *adcLmem;
    int fd_adcR = 0;
    volatile unsigned *adcRmem;
    int fd_syncgo = 0;
    volatile unsigned *syncgomem;
    
    ///////////// set up ADC left
    fd_adcL = open("/dev/uio1", O_RDWR);
    if (fd_adcL < 1) {
        perror(argv[0]);
        printf("Invalid UIO device file: '%s'\n", "uio1");
        return -1;
    }

    adcLmem = (volatile unsigned *)mmap(NULL, MAP_SIZE, 
                  PROT_READ|PROT_WRITE, MAP_SHARED, fd_adcL, 0);
    if (!adcLmem ) {
        perror(argv[0]);
        printf("mmap error\n");
        return -1;
    }

    if ((adcLmem[REG_ID] & 0xFF000000) == 0x05000000)
    {
        printf("! Found ADC Left\n");
    } else 
    {
        printf("! Error: wrong module ID for L (0x%08x)\n",adcLmem[REG_ID]);
        return -1;
    }

    ////////////// set up ADC right
    fd_adcR = open("/dev/uio5", O_RDWR);
    if (fd_adcR < 1) {
        perror(argv[0]);
        printf("Invalid UIO device file: '%s'\n", "uio5");
        return -1;
    }

    adcRmem = (volatile unsigned *)mmap(NULL, MAP_SIZE, 
                  PROT_READ|PROT_WRITE, MAP_SHARED, fd_adcR, 0);
    if (!adcRmem ) {
        perror(argv[0]);
        printf("mmap error\n");
        return -1;
    }

    if ((adcRmem[REG_ID] & 0xFF000000) == 0x05000000)
    {
        printf("! Found ADC Right\n");
    } else 
    {
        printf("! Error: wrong module ID for R\n");
        return -1;
    }

    ////////////// set up syncgo
    fd_syncgo = open("/dev/uio6", O_RDWR);
    if (fd_syncgo < 1) {
        perror(argv[0]);
        printf("Invalid UIO device file: '%s'\n", "uio6");
        return -1;
    }

    syncgomem = (volatile unsigned *)mmap(NULL, MAP_SIZE,
                  PROT_READ|PROT_WRITE, MAP_SHARED, fd_syncgo, 0);
    if (!syncgomem ) {
        perror(argv[0]);
        printf("mmap error\n");
        return -1;
    }

    if ((syncgomem[REG_ID] & 0xFF000000) == 0x06000000)
    {
        printf("! Found sync generator\n");
    } else
    {
        printf("! Error: wrong module ID for sync\n");
        return -1;
    }


    i = 0;
    if (!((adcLmem[REG_STATUS] & 0x00030000) == 0x00030000))
    {
        printf("! FIFO left not empty, emptying...\n");
        while (!((adcLmem[REG_STATUS] & 0x00030000) == 0x00030000))
        {
            adcLmem[REG_STATUS] = 0x1;            // initiate read
            while (!(adcLmem[REG_STATUS] & 0x100)) ; // wait for ack
	    //temp = uiomem[REG_READ];
 	    //printf("0x%04x 0x%04x\n",temp >> 16, temp & 0xFFFF);
            adcLmem[REG_STATUS] = 0x0;           // signal read done
            while (adcLmem[REG_STATUS] & 0x100) ; // wait for ack lowering
        }
    }
    if (!((adcRmem[REG_STATUS] & 0x00030000) == 0x00030000))
    {
        printf("! FIFO right not empty, emptying...\n");
        while (!((adcRmem[REG_STATUS] & 0x00030000) == 0x00030000))
        {
            adcRmem[REG_STATUS] = 0x1;            // initiate read
            while (!(adcRmem[REG_STATUS] & 0x100)) ; // wait for ack
	    //temp = uiomem[REG_READ];
 	    //printf("0x%04x 0x%04x\n",temp >> 16, temp & 0xFFFF);
            adcRmem[REG_STATUS] = 0x0;           // signal read done
            while (adcRmem[REG_STATUS] & 0x100) ; // wait for ack lowering
        }
    }


    printf("! Initiating ADC capture...\n");
    syncgomem[REG_STATUS] = 0x4;
    while (!((adcLmem[REG_STATUS] & 0x03000000) == 0x03000000));
    syncgomem[REG_STATUS] = 0x0;

    while (!((adcLmem[REG_STATUS] & 0x00030000) == 0x00030000))
    {
            adcLmem[REG_STATUS] = 0x1;            // initiate read
            while (!(adcLmem[REG_STATUS] & 0x100)) ; // wait for ack
	    tempL = adcLmem[REG_READ];
            adcLmem[REG_STATUS] = 0x0;           // signal read done
            while (adcLmem[REG_STATUS] & 0x100) ; // wait for ack lowering

            adcRmem[REG_STATUS] = 0x1;            // initiate read
            while (!(adcRmem[REG_STATUS] & 0x100)) ; // wait for ack
	    tempR = adcRmem[REG_READ];
            adcRmem[REG_STATUS] = 0x0;           // signal read done
            while (adcRmem[REG_STATUS] & 0x100) ; // wait for ack lowering

 	    printf("0x%04x 0x%04x 0x%04x 0x%04x\n",tempL >> 16,
                                                   tempL & 0xFFFF,
                                                   tempR >> 16,
                                                   tempR & 0xFFFF);
	    i++;
    }
    printf("! FIFO empty. %d values read.\n",i);

    if  (!((adcLmem[REG_STATUS] & 0x00030000) == 0x00030000))
    {
        printf("Error: data in FIFO right\n");
    }

    munmap((void*)adcLmem, MAP_SIZE);
    munmap((void*)adcRmem, MAP_SIZE);
    munmap((void*)syncgomem, MAP_SIZE);

    return 0;
}

