#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/time.h>
#include <limits.h>

#define MAP_SIZE 0x1000

void usage(void)
{
    printf("usage: test_counters -d <UIO_DEV_FILE>\n");
}

int main(int argc, char *argv[])
{
    int c;
    int i;
    int fd = 0;
    char *uiod = 0;
    int value = 0;
    unsigned start, end;

    volatile unsigned *counters;

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
    counters = (volatile unsigned *)mmap(NULL, MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
    if (!counters) {
        perror(argv[0]);
        printf("mmap\n");
        return -1;
    }

    printf("rd-rd delay on 100 MHz counter: ");
    for (i = 0; i < 20; ++i) {
        start = counters[0];
        end = counters[0];
        printf("%u ", end - start);
    }
    printf("\n");

    printf("rd-rd delay on LVDS counter: ");
    for (i = 0; i < 20; ++i) {
        start = counters[1];
        end = counters[1];
        printf("%u ", end - start);
    }
    printf("\n");

    printf("Estimate clock speed 1:");
    start = counters[0];
    sleep(1);
    end = counters[0];
    if (start > end) {
	value = UINT_MAX - start + end;
    } else {
	value = end - start;
    }
    printf("%f MHz\n",(float)(value / 1e6));

    printf("Estimate clock speed 2:");
    start = counters[1];
    sleep(1);
    end = counters[1];
    if (start > end) {
	value = UINT_MAX - start + end;
    } else {
	value = end - start;
    }
    printf("%f MHz\n",(float)(value / 1e6));

    munmap((void*)counters, MAP_SIZE);
    return 0;
}

