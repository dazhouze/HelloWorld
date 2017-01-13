#include<stdio.h>
#include<string.h>

struct read{
    char id[20];
    int len;
    int pos;
    struct read *next;
};

int main ()
{
    struct read fir, sec, thr , *head;
    printf("size of struct:%lu\n",sizeof(fir));
    head = &fir;
    char name[10] = "q9514";
    strcpy(fir.id, name);
    fir.len = 100;
    fir.pos = 123;
    fir.next = &sec;
    //sec->id="9515";
    sec.len = 101;
    sec.pos = 1234;
    sec.next = &thr;
    //thr->id="9516";
    thr.len = 102;
    thr.pos = 12345;
    thr.next = NULL;

    struct read *p;
    p = head;
    while (p!=NULL){
        printf("id:%s\tlen:%d\tpos:%d\n", p->id, p->len, p->pos);
        p = p->next;
    }

    return 0;
}
