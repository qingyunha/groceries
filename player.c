#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <dirent.h>
#include <string.h>
#include <errno.h>
#include <signal.h>

#define err(msg) \
  do {perror(msg); exit(1);}while(0);

typedef struct node{
  char name[128];
  struct node *pre;
  struct node *next;
}Node;


void addNode(Node **h, char *name)
{
  Node *p = malloc(sizeof(Node));
  if(*h == NULL){
    p->next = p;
    p->pre = p;
    *h = p;
  }else{
    p->next = *h;
    p->pre = (*h)->pre;
    (*h)->pre->next = p;
    (*h)->pre = p;
  }
  strncpy(p->name, name, strlen(name));

}

#define SONGS "."

Node *getlist()
{
  Node *h = NULL;
  DIR *d; 
  struct dirent *item;
  int i;

  if( (d = opendir(SONGS)) == NULL)
    err("opendir error")

  while( (item = readdir(d)) != NULL){
    if(strchr(item->d_name,'.') == item->d_name)
      continue;
    addNode(&h, item->d_name);
  }
  return h;
}

int main()
{
  int opt; 
  int flags = 0;  //0 stop, 1 play, 2 pause
  pid_t pid = -1;
  //int fd = openkbd();
  Node *songlist = getlist();


  while(1){
    printf("1.play               2.stop\n");
    printf("3.pause              4.continue\n");
    printf("5.pre                6.next\n");
    printf("0.exit\n");
    printf("please chose: ");
    scanf("%d", &opt);
    //opt = getkey();
    printf("\n");

    switch(opt){
    case 0:
        if(pid > 0){
          kill(pid,SIGKILL);
          waitpid(pid, NULL, 0);
        }
	//close(fd);
        return 0;

    case 1:
play:
        if(flags != 0){
          printf("already played\n");
        }else{
          if( (pid = fork()) < 0){
            perror("fork error");
          }else if(pid == 0){
            while(1){
              printf("\nI am sing %s", songlist->name);
              sleep(2);
            }
            exit(0);
          }
        }
        flags = 1;
        break;

    case 2:
        if(flags > 0 && pid > 0){
          kill(pid,SIGKILL);
          waitpid(pid, NULL, 0);
          pid = -1;
          flags = 0;
        }
        break;

    case 3:
        if(flags = 1 && pid > 0){
          kill(pid, SIGSTOP);
          flags = 2;
        }
        break;

    case 4:
        if(flags = 2 && pid > 0){
          kill(pid, SIGCONT);
          flags = 1;
        }
        break;

    case 5:
        if(pid > 0){
          kill(pid, SIGKILL);
          waitpid(pid, NULL, 0);
          pid = -1;
        }
        songlist = songlist->pre;
        flags = 0;
        goto play;

    case 6:
        if(pid > 0){
          kill(pid, SIGKILL);
          waitpid(pid, NULL, 0);
          pid = -1;
        }
        songlist = songlist->next;
        flags = 0;
        goto play;

   default:
        break;
    }
  }
}