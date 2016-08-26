#include<stdio.h>
#include<ctype.h>
#include<string.h>

#include"getword.h"

#define MAXWORD 100
struct tnode *addtree(struct tnode *, char *);
void treeprint(struct tnode *);
int getword(char *, int);
main(){
    struct tnode *root;
    char word[MAXWORD];
    root = NULL;
    while (getword(word, MAXWORD) != EOF)
        if (isalpha(word[0]))
            root = addtree(root, word);
    treeprint(root);
    return 0;
}
struct tnode *talloc(void);
char *strdup(char *);
struct tnode *addtree(struct tnode *p, char *w)
{
    int  cond;
    if (p == NULL){
        p = talloc();
        p->word = strdup(w);
        p->count = 1;
        p->left = p->rigth =NULL;//mark
    } else if ((cond = strcmp(w, p->word)) == 0){
    }
}
