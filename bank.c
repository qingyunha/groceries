#include<stdio.h>

#define N 5
#define M 3

#define MIN(a,b) (a) < (b)? (a): (b)

int ava[M] = {3,3,2};

int max[N * M] = {
            7,5,3,
            3,2,2,
            9,0,2,
            2,2,2,
            4,3,3,
          };

int alloc[N * M] = {       
              0,1,0,
              2,0,0,
              3,0,2,
              2,1,1,
              0,0,2,
            };

int need[N * M] = {
                    7,4,3,
                    1,2,2,
                    6,0,0,
                    0,1,1,
                    4,3,1,
                  };

int secure(){
  int work[M];
  int i,j,flag = 0;
  for(i = 0; i < M; i++)
    work[i] = ava[i];

  int finish[N] = {0,0,0,0,0};

find:
  flag = 0;
  for(i = 0; i < N; i++){
    if(finish[i] == 0){
      flag = 1;
      for(j = 0; j < M; j++)
        if(need[i*M+j] > work[j]){
          flag = 0;
          break;
        }
    }
    if(flag)
      break;
  }
  if(flag){
    for(j = 0; j < M; j++)
      work[j] += alloc[i*M+j];
    finish[i] = 1;
    goto find;
  }

  flag = 1;
  for(i = 0; i < N; i++){
    if(finish[i] == 0)
      flag = 0;
  }
  return flag;
}

void pp(){
  int i;
  printf("available: %d %d %d\n",ava[0], ava[1], ava[2]);
  for(i = 0; i < N; i++){
   printf("%d %d %d ",alloc[i*M+0], alloc[i*M+1],alloc[i*M+2]);
   printf(" %d %d %d\n",need[i*M+0], need[i*M+1],need[i*M+2]);
  }
}

int finish(int i)
{
  int j, r = 1;
  for(j = 0; j < M; j++)
    if( !(r = r && (need[i*M+j] == 0)))
        break;

  return r;
}

void fre(int i)
{
  int j, r = 1;
  for(j = 0; j < M; j++){
    ava[j] += alloc[i*M+j];
    alloc[i*M+j] = 0;
  }
}

int main(int argc, char* argv[])
{
  int i,j;
  int req[M];
  if(argc > 1)
    srand(atoi(argv[1]));

  if(secure() == 0)
    return -1;

      pp();

  while(1){
    for(i = 0; i < N; i++){
      if(finish(i))
        continue;
      printf("*******proc %d running******\n",i);
      for(j = 0; j < M; j++){
        if(need[i*M+j] == 0 || ava[j] == 0)
          req[j] = 0;
        else{
          int k=MIN(ava[j],need[i*M+j]);
          req[j] = (rand() % k) + 1;
        }
        alloc[i*M+j] += req[j];
        need[i*M+j] -= req[j];
        ava[j] -= req[j];
      }
      
      if(secure() == 0){
        for(j = 0; j < M; j++){
          alloc[i*M+j] -= req[j];
          need[i*M+j] += req[j];
          ava[j] += req[j];
        }
        printf("proc %d sleeping\n\n",i);
        //pp();  
      }else{
        if(finish(i))
          fre(i);
        printf("%d %d %d to proc %d\n\n",req[0],req[1],req[2],i);
        pp();
      }
      
      printf("\n");
      //getchar();
    }//for N

    if(ava[0] == 10 && ava[1] == 5 && ava[2] == 7)
      break;
  }

  return 0;
}

