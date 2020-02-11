#include <stdlib.h>     //exit()
#include <signal.h>     //signal()
#include <time.h>
#include "ADS1256.h"
#include "stdio.h"
#include <time.h>
#include <string.h>
#include <sys/timeb.h>
#include <sys/time.h>

void  Handler(int signo)
{
    //System Exit
    fprintf(stderr, "\r\nEND                  \r\n");
    DEV_ModuleExit();

    exit(0);
}

int main(int argc, char** argv)
{ 
    //UDOUBLE ADC[8],i;
    fprintf(stderr, "demo\r\n");
    DEV_ModuleInit();

    // Exception handling:ctrl + c
    signal(SIGINT, Handler);

    if(ADS1256_init() == 1){
        fprintf(stderr, "\r\nEND                  \r\n");
        DEV_ModuleExit();
        exit(0);
    }
    int totalSize = 100;
    if (argc > 1){
        totalSize = atoi(argv[1]);
    }

    double current[totalSize];
    double voltage[totalSize];
    double times[totalSize];

    struct timeval stop1, start1;
    gettimeofday(&start1, NULL);
    clock_t clks = clock();
    for(int i = 0; i < totalSize; i++){
        gettimeofday(&stop1, NULL);
        times[i] = (stop1.tv_sec - start1.tv_sec) + (stop1.tv_usec - start1.tv_usec)/1000000.0;
        current[i] = ADS1256_GetChannalValue(0)*5.0/0x7fffff;
        voltage[i] = ADS1256_GetChannalValue(1)*5.0/0x7fffff;
        //voltage[i] = ADS1256_GetChannalValue(3)*5.0/0x7fffff;
    }
    clks = clock() - clks;
    gettimeofday(&stop1, NULL);
    //FILE* file = fopen("data.txt", "w");
    double totalTime = (stop1.tv_sec - start1.tv_sec) + (stop1.tv_usec - start1.tv_usec)/1000000.0;

    FILE* dataFile = fopen("data", "w");

    for(int i = 0; i < totalSize; i++){
        //fputs("%f\t%f\t%f\n", times[i], current[i], voltage[i]);
        fprintf(dataFile, "%f\t%f\t%f\n", times[i], current[i], voltage[i]);
    }
    
    fclose(dataFile);

    fprintf(stderr, "Total clocks: %ld With time: %f seconds (%f samples per second)\n", clks, totalTime, totalSize/(totalTime));
    //fclose(file);

    /*while(1){
    

        
         printf("0 : %f\r\n",ADS1256_GetChannalValue(0)*5.0/0x7fffff);
         printf("1 : %f\r\n",ADS1256_GetChannalValue(1)*5.0/0x7fffff);
        // printf("2 : %f\r\n",ADS1256_GetChannalValue(2)*5.0/0x7fffff);
        // printf("3 : %f\r\n",ADS1256_GetChannalValue(3)*5.0/0x7fffff);
        // printf("4 : %f\r\n",ADS1256_GetChannalValue(4)*5.0/0x7fffff);
        // printf("5 : %f\r\n",ADS1256_GetChannalValue(5)*5.0/0x7fffff);
        // printf("6 : %f\r\n",ADS1256_GetChannalValue(6)*5.0/0x7fffff);
        // printf("7 : %f\r\n",ADS1256_GetChannalValue(7)*5.0/0x7fffff);


        //ADS1256_GetAll(ADC);
        
             
        
        
        //for(i=0;i<8;i++){
            //printf("%d %f\r\n",i,ADC[i]*5.0/0x7fffff);
        //}
        //printf("\33[8A");//Move the cursor up 8 lines
    }*/
    return 0;
}
